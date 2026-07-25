import sys
import os

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QComboBox, QStackedWidget, QLineEdit, QRadioButton, QButtonGroup, QListWidget,
    QLabel, QSpinBox, QPushButton, QMessageBox, QGroupBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from linetool.geometry import single_circuit_gmd, double_vertical_gmd, double_horizontal_gmd
from linetool.bundling import bundle_gmr, double_circuit_gmr
from linetool.electrical import inductance_capacitance
from linetool.acsr_data import ACSR_TABLE, get_conductor, ACSR_IMAGE_PATH

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")


class LineToolWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transmission Line Parameters Tool")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)

        # --- Config selector ---
        config_group = QGroupBox("Configuration")
        config_form = QFormLayout()
        self.config_combo = QComboBox()
        self.config_combo.addItems([
            "Single-circuit",
            "Double-circuit vertical",
            "Double-circuit horizontal",
        ])
        self.config_combo.currentIndexChanged.connect(self.on_config_changed)
        config_form.addRow("Circuit type:", self.config_combo)

        self.variant_combo = QComboBox()
        self.variant_combo.addItems(["Variant 1", "Variant 2"])
        config_form.addRow("Transposition:", self.variant_combo)

        config_group.setLayout(config_form)
        left_layout.addWidget(config_group)

        # --- Geometry input panel (stacked by config type) ---
        geometry_group = QGroupBox("Geometry")
        geometry_layout = QVBoxLayout()

        self.geometry_stack = QStackedWidget()

        # Page 0: single-circuit
        single_page = QWidget()
        single_form = QFormLayout(single_page)
        self.single_D12 = QLineEdit()
        self.single_D23 = QLineEdit()
        self.single_D13 = QLineEdit()
        single_form.addRow("D12:", self.single_D12)
        single_form.addRow("D23:", self.single_D23)
        single_form.addRow("D13:", self.single_D13)
        self.geometry_stack.addWidget(single_page)

        # Page 1: double-circuit vertical
        vert_page = QWidget()
        vert_form = QFormLayout(vert_page)
        self.vert_S11 = QLineEdit()
        self.vert_S22 = QLineEdit()
        self.vert_S33 = QLineEdit()
        self.vert_H12 = QLineEdit()
        self.vert_H23 = QLineEdit()
        vert_form.addRow("S11:", self.vert_S11)
        vert_form.addRow("S22:", self.vert_S22)
        vert_form.addRow("S33:", self.vert_S33)
        vert_form.addRow("H12:", self.vert_H12)
        vert_form.addRow("H23:", self.vert_H23)
        self.geometry_stack.addWidget(vert_page)

        # Page 2: double-circuit horizontal
        horiz_page = QWidget()
        horiz_form = QFormLayout(horiz_page)
        self.horiz_D12 = QLineEdit()
        self.horiz_D23 = QLineEdit()
        self.horiz_D13 = QLineEdit()
        self.horiz_S11 = QLineEdit()
        horiz_form.addRow("D12:", self.horiz_D12)
        horiz_form.addRow("D23:", self.horiz_D23)
        horiz_form.addRow("D13:", self.horiz_D13)
        horiz_form.addRow("S11:", self.horiz_S11)
        self.geometry_stack.addWidget(horiz_page)

        geometry_layout.addWidget(self.geometry_stack)

        # Unit toggle for geometry
        unit_layout = QHBoxLayout()
        self.unit_m = QRadioButton("m")
        self.unit_ft = QRadioButton("ft")
        self.unit_m.setChecked(True)
        self.geometry_unit_group = QButtonGroup()
        self.geometry_unit_group.addButton(self.unit_m)
        self.geometry_unit_group.addButton(self.unit_ft)
        unit_layout.addWidget(QLabel("Spacing unit:"))
        unit_layout.addWidget(self.unit_m)
        unit_layout.addWidget(self.unit_ft)
        geometry_layout.addLayout(unit_layout)

        geometry_group.setLayout(geometry_layout)
        left_layout.addWidget(geometry_group)

        # --- Conductor panel ---
        conductor_group = QGroupBox("Conductor (ACSR)")
        conductor_layout = QVBoxLayout()

        self.conductor_list = QListWidget()
        for name in sorted(ACSR_TABLE.keys()):
            self.conductor_list.addItem(name)
        self.conductor_list.currentTextChanged.connect(self.on_conductor_selected)
        conductor_layout.addWidget(self.conductor_list)

        self.conductor_info_label = QLabel("Select a conductor to see its specs.")
        self.conductor_info_label.setWordWrap(True)
        conductor_layout.addWidget(self.conductor_info_label)

        bundle_form = QFormLayout()
        self.bundle_count = QSpinBox()
        self.bundle_count.setRange(1, 4)
        self.bundle_count.setValue(1)
        self.bundle_count.valueChanged.connect(self.on_bundle_count_changed)
        bundle_form.addRow("Bundle count:", self.bundle_count)

        self.bundle_spacing = QLineEdit()
        self.bundle_spacing.setEnabled(False)
        bundle_form.addRow("Bundle spacing:", self.bundle_spacing)

        cond_unit_layout = QHBoxLayout()
        self.cond_unit_cm = QRadioButton("cm")
        self.cond_unit_in = QRadioButton("in")
        self.cond_unit_cm.setChecked(True)
        self.cond_unit_group = QButtonGroup()
        self.cond_unit_group.addButton(self.cond_unit_cm)
        self.cond_unit_group.addButton(self.cond_unit_in)
        cond_unit_layout.addWidget(QLabel("Conductor/bundle unit:"))
        cond_unit_layout.addWidget(self.cond_unit_cm)
        cond_unit_layout.addWidget(self.cond_unit_in)

        conductor_layout.addLayout(bundle_form)
        conductor_layout.addLayout(cond_unit_layout)

        conductor_group.setLayout(conductor_layout)
        left_layout.addWidget(conductor_group)

        # --- Calculate button ---
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.on_calculate)
        left_layout.addWidget(self.calculate_button)

        # --- Right side: image + results ---
        image_group = QGroupBox("ACSR Conductor")
        image_layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_path = os.path.join(ASSETS_DIR, ACSR_IMAGE_PATH)
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaledToWidth(300))
        else:
            self.image_label.setText(f"(image not found: {image_path})")
        image_layout.addWidget(self.image_label)
        image_group.setLayout(image_layout)
        right_layout.addWidget(image_group)

        results_group = QGroupBox("Results")
        results_form = QFormLayout()
        self.result_gmd = QLabel("-")
        self.result_gmrl = QLabel("-")
        self.result_gmrc = QLabel("-")
        self.result_L = QLabel("-")
        self.result_C = QLabel("-")
        results_form.addRow("GMD:", self.result_gmd)
        results_form.addRow("GMRL:", self.result_gmrl)
        results_form.addRow("GMRC:", self.result_gmrc)
        results_form.addRow("L (mH/km):", self.result_L)
        results_form.addRow("C (uF/km):", self.result_C)
        results_group.setLayout(results_form)
        right_layout.addWidget(results_group)

        right_layout.addStretch()

        self.on_config_changed(0)

    def on_config_changed(self, index: int):
        self.geometry_stack.setCurrentIndex(index)
        self.variant_combo.setEnabled(index != 0)  # single-circuit has no transposition variant

    def on_bundle_count_changed(self, value: int):
        self.bundle_spacing.setEnabled(value > 1)

    def on_conductor_selected(self, name: str):
        if not name:
            return
        try:
            spec = get_conductor(name)
        except KeyError:
            return
        self.conductor_info_label.setText(
            f"<b>{name}</b><br>"
            f"CMIL: {spec.cmil} | Strand: {spec.strand}<br>"
            f"Diameter: {spec.diameter_cm} cm | GMR: {spec.gmr_cm} cm<br>"
            f"Resistance: {spec.resistance_25c} / {spec.resistance_50c} ohm/km (25C/50C)<br>"
            f"Ampacity: {spec.ampacity} A"
        )

    def _read_float(self, widget: QLineEdit, field_name: str) -> float:
        text = widget.text().strip()
        if not text:
            raise ValueError(f"'{field_name}' is required")
        try:
            return float(text)
        except ValueError:
            raise ValueError(f"'{field_name}' must be a number")

    def on_calculate(self):
        try:
            config_index = self.config_combo.currentIndex()
            variant = self.variant_combo.currentIndex() + 1  # 1 or 2

            geometry_unit = "m" if self.unit_m.isChecked() else "ft"

            # --- Geometry ---
            Da1a2 = Db1b2 = Dc1c2 = None
            if config_index == 0:  # single-circuit
                D12 = self._read_float(self.single_D12, "D12")
                D23 = self._read_float(self.single_D23, "D23")
                D13 = self._read_float(self.single_D13, "D13")
                GMD = single_circuit_gmd(D12, D23, D13)
            elif config_index == 1:  # double-vertical
                S11 = self._read_float(self.vert_S11, "S11")
                S22 = self._read_float(self.vert_S22, "S22")
                S33 = self._read_float(self.vert_S33, "S33")
                H12 = self._read_float(self.vert_H12, "H12")
                H23 = self._read_float(self.vert_H23, "H23")
                GMD, Da1a2, Db1b2, Dc1c2 = double_vertical_gmd(S11, S22, S33, H12, H23, variant)
            else:  # double-horizontal
                D12 = self._read_float(self.horiz_D12, "D12")
                D23 = self._read_float(self.horiz_D23, "D23")
                D13 = self._read_float(self.horiz_D13, "D13")
                S11 = self._read_float(self.horiz_S11, "S11")
                GMD, Da1a2, Db1b2, Dc1c2 = double_horizontal_gmd(D12, D23, D13, S11, variant)

            # --- Conductor ---
            selected_items = self.conductor_list.selectedItems()
            if not selected_items:
                raise ValueError("Please select a conductor from the list")
            spec = get_conductor(selected_items[0].text())

            r = spec.diameter_cm / 2
            Ds = spec.gmr_cm
            cond_unit_is_cm = self.cond_unit_cm.isChecked()

            nb = self.bundle_count.value()
            d = 0.0
            if nb > 1:
                d = self._read_float(self.bundle_spacing, "Bundle spacing")

            # Convert conductor values to match geometry unit.
            # NOTE: diameter/GMR from the ACSR table are always in cm (fixed by the
            # data source), regardless of the cm/in toggle -- that toggle only
            # applies to the user-typed bundle spacing.
            if geometry_unit == "m":
                cm_factor = 0.01
                in_factor = 0.0254
            else:  # ft
                cm_factor = 1 / 30.48
                in_factor = 1 / 12

            r *= cm_factor
            Ds *= cm_factor
            d *= cm_factor if cond_unit_is_cm else in_factor

            Dsb, rb = bundle_gmr(Ds=Ds, r=r, nb=nb, d=d)

            if config_index == 0:  # single-circuit: no double-circuit combination
                GMRL, GMRC = Dsb, rb
            else:
                GMRL, GMRC = double_circuit_gmr(Dsb, rb, Da1a2, Db1b2, Dc1c2)

            # --- Electrical ---
            L, C = inductance_capacitance(GMD, GMRL, GMRC)

            self.result_gmd.setText(f"{GMD:.5f} {geometry_unit}")
            self.result_gmrl.setText(f"{GMRL:.5f} {geometry_unit}")
            self.result_gmrc.setText(f"{GMRC:.5f} {geometry_unit}")
            self.result_L.setText(f"{L:.4f}")
            self.result_C.setText(f"{C:.4f}")

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unexpected error: {e}")


def main():
    app = QApplication(sys.argv)
    window = LineToolWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()