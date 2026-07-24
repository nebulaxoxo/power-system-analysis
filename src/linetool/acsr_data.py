from dataclasses import dataclass


@dataclass(frozen=True)
class ConductorSpec:
    cmil: int
    strand: str            # e.g. "45/7"
    diameter_cm: float
    gmr_cm: float
    resistance_25c: float  # ohm/km at 60Hz, 25C
    resistance_50c: float  # ohm/km at 60Hz, 50C
    ampacity: int


ACSR_TABLE: dict[str, ConductorSpec] = {
    "JOREE":     ConductorSpec(2515000, "76/19", 4.7752, 1.8928, 0.02600, 0.02800, 1550),
    "THRASHER":  ConductorSpec(2312000, "76/19", 4.5771, 1.8135, 0.02770, 0.03000, 1500),
    "KIWI":      ConductorSpec(2167000, "72/7",  4.4069, 1.7374, 0.02940, 0.03190, 1465),
    "BLUEBIRD":  ConductorSpec(2156000, "84/19", 4.4755, 1.7920, 0.02900, 0.03140, 1475),
    "CHUKAR":    ConductorSpec(1781000, "84/19", 4.0691, 1.6276, 0.03410, 0.03720, 1405),
    "FALCON":    ConductorSpec(1590000, "54/19", 3.9243, 1.5847, 0.03740, 0.04080, 1380),
    "LAPWING":   ConductorSpec(1590000, "54/19", 3.8200, 1.5150, 0.03870, 0.04210, 1340),
    "PARROT":    ConductorSpec(1510500, "54/19", 3.8252, 1.5453, 0.03860, 0.04280, 1340),
    "BOBOLINK":  ConductorSpec(1431000, "45/7",  3.6250, 1.4390, 0.04260, 0.04640, 1250),
    "PLOVER":    ConductorSpec(1431000, "54/19", 3.7210, 1.5026, 0.04077, 0.04723, 1300),
    "MARTIN":    ConductorSpec(1351000, "54/19", 3.6170, 1.4600, 0.04319, 0.05000, 1250),
    "PHEASANT":  ConductorSpec(1272000, "54/19", 3.5103, 1.4173, 0.04586, 0.05290, 1200),
    "BITTERN":   ConductorSpec(1272000, "45/7",  3.4160, 1.3560, 0.04750, 0.05190, 1100),
    "GRACKLE":   ConductorSpec(1192500, "54/19", 3.3985, 1.3716, 0.04897, 0.05630, 1160),
    "FINCH":     ConductorSpec(1113000, "54/19", 3.2842, 1.3258, 0.05245, 0.06020, 1110),
    "BLUEJAY":   ConductorSpec(1113000, "45/7",  3.1950, 1.2680, 0.05380, 0.05890, 1100),
    "CURLEW":    ConductorSpec(1033500, "54/7",  3.1648, 1.2800, 0.05650, 0.06432, 1060),
    "ORTOLAN":   ConductorSpec(1033500, "45/7",  3.0780, 1.2220, 0.05780, 0.06330, 1050),
    "CARDINAL":  ConductorSpec(954000,  "54/7",  3.0378, 1.2283, 0.06103, 0.07000, 1010),
    "RAIL":      ConductorSpec(954000,  "45/7",  2.9590, 1.1730, 0.06240, 0.06830, 1000),
    "CANARY":    ConductorSpec(900000,  "54/7",  2.9515, 1.1917, 0.06463, 0.07365, 970),
    "CRANE":     ConductorSpec(874500,  "54/7",  2.9108, 1.1765, 0.06712, 0.07632, 950),
    "CONDOR":    ConductorSpec(795000,  "54/7",  2.7762, 1.1216, 0.07396, 0.08564, 900),
    "DRAKE":     ConductorSpec(795000,  "26/7",  2.8143, 1.1430, 0.07272, 0.08000, 900),
    "MALLARD":   ConductorSpec(795000,  "30/19", 2.8956, 1.1978, 0.07272, 0.08000, 910),
    "TERN":      ConductorSpec(795000,  "45/7",  2.7000, 1.0730, 0.07440, 0.08160, 900),
    "CROW":      ConductorSpec(715500,  "54/7",  2.6314, 1.0637, 0.08204, 0.09211, 830),
    "STARLING":  ConductorSpec(715500,  "26/7",  2.6695, 1.0820, 0.08142, 0.08962, 840),
    "REDWING":   ConductorSpec(715500,  "30/19", 2.7457, 1.1338, 0.08142, 0.08962, 840),
    "FLAMINGO":  ConductorSpec(666600,  "54/7",  2.5400, 1.0272, 0.08763, 0.09950, 800),
    "ROOK":      ConductorSpec(636000,  "54/7",  2.4816, 1.0028, 0.09198, 0.10490, 770),
    "GROSBEAK":  ConductorSpec(636000,  "26/7",  2.5146, 1.0210, 0.09136, 0.10055, 780),
    "EGRET":     ConductorSpec(636000,  "30/19", 2.5883, 1.0698, 0.09136, 0.10055, 780),
    "PEACOCK":   ConductorSpec(605000,  "54/7",  2.4206, 0.9784, 0.09633, 0.11032, 750),
    "SQUAB":     ConductorSpec(605000,  "26/7",  2.4536, 0.9967, 0.09571, 0.10690, 760),
    "DOVE":      ConductorSpec(556500,  "26/7",  2.3546, 0.9540, 0.10441, 0.11554, 730),
    "EAGLE":     ConductorSpec(556500,  "30/7",  2.4206, 0.9997, 0.10441, 0.11554, 730),
    "PARAKEET":  ConductorSpec(556500,  "24/7",  2.3220, 0.9330, 0.10530, 0.11560, 715),
    "OSPREY":    ConductorSpec(556500,  "18/1",  2.2330, 0.8660, 0.10520, 0.11540, 700),
    "HAWK":      ConductorSpec(477000,  "26/7",  2.1793, 0.8839, 0.12270, 0.13480, 670),
    "HEN":       ConductorSpec(477000,  "30/7",  2.2428, 0.9266, 0.12290, 0.13490, 670),
    "PELICAN":   ConductorSpec(477000,  "18/1",  2.0680, 0.8020, 0.12240, 0.13440, 640),
    "IBIS":      ConductorSpec(397500,  "26/7",  1.9888, 0.8077, 0.14720, 0.16170, 590),
    "LARK":      ConductorSpec(397500,  "30/7",  2.0472, 0.8473, 0.14740, 0.16190, 600),
    "CHICKADEE": ConductorSpec(397500,  "18/1",  1.8872, 0.7345, 0.14555, 0.15985, 575),
    "LINNET":    ConductorSpec(336400,  "26/7",  1.8313, 0.7437, 0.17380, 0.19090, 530),
    "ORIOLE":    ConductorSpec(336400,  "30/7",  1.8821, 0.7772, 0.17400, 0.19120, 530),
    "OSTRICH":   ConductorSpec(300000,  "26/7",  1.7272, 0.7010, 0.19480, 0.21400, 490),
    "PIPER":     ConductorSpec(300000,  "30/7",  1.7780, 0.7345, 0.19510, 0.21440, 500),
    "PARTRIDGE": ConductorSpec(266800,  "26/7",  1.6307, 0.6614, 0.21890, 0.24050, 460),
    "WAXWING":   ConductorSpec(266800,  "18/1",  1.5468, 0.6035, 0.21678, 0.23810, 450),
    "MERLIN":    ConductorSpec(336400,  "18/1",  1.6460, 0.6740, 0.17310, 0.19010, 460),
}

ACSR_IMAGE_PATH = "ACSR1.jpg"  # single shared image for all conductors


def get_conductor(name: str) -> ConductorSpec:
    """
    Case-insensitive lookup by conductor code name.
    Raises KeyError if not found (caller/GUI handles this as a user-facing popup).
    """
    key = name.strip().upper()
    if key not in ACSR_TABLE:
        raise KeyError(f"ACSR conductor '{name}' not found")
    return ACSR_TABLE[key]