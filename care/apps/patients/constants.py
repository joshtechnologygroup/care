from collections import namedtuple

CURRENT_HEALTH_CHOICES = namedtuple("type", ["ND", "RV", "WR", "SQ", "BT"])(0, 1, 2, 3, 4)


CATEGORY_CHOICES = [
    ("Mild", "Category-A"),
    ("Moderate", "Category-B"),
    ("Severe", "Category-C"),
    (None, "UNCLASSIFIED"),
]

SYMPTOM_TYPE_CHOICES = namedtuple(
    "type", ["AS", "FV", "ST", "CO", "BT", "MY", "AD", "VD", "OT", "SA", "SP", "NA", "CP", "HP", "ND", "BA",],
)(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)

SYMPTOM_CHOICES = [
    (SYMPTOM_TYPE_CHOICES.AS, "ASYMPTOMATIC"),
    (SYMPTOM_TYPE_CHOICES.FV, "FEVER"),
    (SYMPTOM_TYPE_CHOICES.ST, "SORE THROAT"),
    (SYMPTOM_TYPE_CHOICES.CO, "COUGH"),
    (SYMPTOM_TYPE_CHOICES.BT, "BREATHLESSNESS"),
    (SYMPTOM_TYPE_CHOICES.MY, "MYALGIA"),
    (SYMPTOM_TYPE_CHOICES.AD, "ABDOMINAL DISCOMFORT"),
    (SYMPTOM_TYPE_CHOICES.VD, "VOMITING/DIARRHOEA"),
    (SYMPTOM_TYPE_CHOICES.OT, "OTHERS"),
    (SYMPTOM_TYPE_CHOICES.SA, "SARI"),
    (SYMPTOM_TYPE_CHOICES.SP, "SPUTUM"),
    (SYMPTOM_TYPE_CHOICES.NA, "NAUSEA"),
    (SYMPTOM_TYPE_CHOICES.CP, "CHEST PAIN"),
    (SYMPTOM_TYPE_CHOICES.HP, "HEMOPTYSIS"),
    (SYMPTOM_TYPE_CHOICES.ND, "NASAL DISCHARGE"),
    (SYMPTOM_TYPE_CHOICES.BA, "BODY ACHE"),
]

DISEASE_CHOICES_MAP = namedtuple("type", ["NO", "DB", "HD", "HT", "KD", "LA", "CA"])(1, 2, 3, 4, 5, 6, 7)

DISEASE_CHOICES = [
    (DISEASE_CHOICES_MAP.NO, "NO DISEASE"),
    (DISEASE_CHOICES_MAP.DB, "DIABETES"),
    (DISEASE_CHOICES_MAP.HD, "HEART DISEASE"),
    (DISEASE_CHOICES_MAP.HT, "HYPERTENSION"),
    (DISEASE_CHOICES_MAP.KD, "KIDNEY DISEASES"),
    (DISEASE_CHOICES_MAP.LA, "LUNG DISEASES/ASTHMA"),
    (DISEASE_CHOICES_MAP.CA, "CANCER"),
]

SuggestionChoices = namedtuple("type", ["HI", "A", "R"])("HI", "A", "R")

SUGGESTION_CHOICES = [
    (SuggestionChoices.HI, "HOME ISOLATION"),
    (SuggestionChoices.A, "ADMISSION"),
    (SuggestionChoices.R, "REFERRAL"),
]

ADMIT_CHOICES = namedtuple("type", ["NA", "IWO", "IO", "IR", "ICU", "ICV", "HI"])(None, 1, 2, 3, 4, 5, 6)

SAMPLE_TYPE_CHOICES = namedtuple("type", ["UN", "BA", "TS", "BE", "AS", "CS", "OT"])(0, 1, 2, 3, 4, 5, 6)

SAMPLE_TEST_RESULT_MAP = namedtuple("type", ["SS", "RP", "PO", "NG", "PP", "TI"])(1, 2, 3, 4, 5, 6)

SAMPLE_FLOW_RULES = {
    # previous rule      # next valid rules
    "REQUEST_SUBMITTED": {"APPROVED", "DENIED",},
    "APPROVED": {"SENT_TO_COLLECTON_CENTRE", "RECEIVED_AND_FORWARED", "RECEIVED_AT_LAB", "COMPLETED",},
    "DENIED": {"REQUEST_SUBMITTED"},
    "SENT_TO_COLLECTON_CENTRE": {"RECEIVED_AND_FORWARED", "RECEIVED_AT_LAB", "COMPLETED",},
    "RECEIVED_AND_FORWARED": {"RECEIVED_AT_LAB", "COMPLETED"},
    "RECEIVED_AT_LAB": {"COMPLETED"},
}

SAMPLE_TEST_FLOW_MAP = namedtuple("type", ["RS", "AP", "DN", "SC", "RF", "RL", "CT"])(1, 2, 3, 4, 5, 6, 7)

SAMPLE_TEST_FLOW_CHOICES = [
    (SAMPLE_TEST_FLOW_MAP.RS, "REQUEST_SUBMITTED"),
    (SAMPLE_TEST_FLOW_MAP.AP, "APPROVED"),
    (SAMPLE_TEST_FLOW_MAP.DN, "DENIED"),
    (SAMPLE_TEST_FLOW_MAP.SC, "SENT_TO_COLLECTON_CENTRE"),
    (SAMPLE_TEST_FLOW_MAP.RF, "RECEIVED_AND_FORWARED"),
    (SAMPLE_TEST_FLOW_MAP.RL, "RECEIVED_AT_LAB"),
    (SAMPLE_TEST_FLOW_MAP.CT, "COMPLETED"),
]

SOURCE_CHOICES = namedtuple("type", ["CA", "CT", "ST"])(10, 20, 30)

DISEASE_STATUS_CHOICES = namedtuple("type", ["NT", "SU", "PO", "NE", "RE", "RD", "EX"])(1, 2, 3, 4, 5, 6, 7)

OCCUPATION_CHOICES = namedtuple("type", ["MW", "GE", "PE", "HM", "WA", "OT"])(2, 3, 4, 5, 6, 7)

RELATION_CHOICES = namedtuple("type", ["FM", "FR", "RL", "NG", "TT", "WH", "WS", "WO", "WP", "OT"])(
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10
)
MODE_CONTACT_CHOICES = namedtuple("type", ["TBF", "DPC", "CUI", "LSH", "CLWP", "CPA", "HCWP", "SSWE", "TTWE"])(
    1, 2, 3, 4, 5, 6, 7, 8, 9
)
# "1. Touched body fluids of the patient (respiratory tract secretions/blood/vomit/saliva/urine/faces)"
TOUCHED_BODY_FLUIDS = 1
# "2. Had direct physical contact with the body of the patient
# including physical examination without full precautions."
DIRECT_PHYSICAL_CONTACT = 2
# "3. Touched or cleaned the linens/clothes/or dishes of the patient"
CLEANED_USED_ITEMS = 3
# "4. Lives in the same household as the patient."
LIVE_IN_SAME_HOUSEHOLD = 4
# "5. Close contact within 3ft (1m) of the confirmed case without precautions."
CLOSE_CONTACT_WITHOUT_PRECAUTION = 5
# "6. Passenger of the aeroplane with a confirmed COVID -19 passenger for more than 6 hours."
CO_PASSENGER_AEROPLANE = 6
# "7. Health care workers and other contacts who had full PPE while handling the +ve case"
HEALTH_CARE_WITH_PPE = 7
# "8. Shared the same space(same class for school/worked in
# same room/similar and not having a high risk exposure"
SHARED_SAME_SPACE_WITHOUT_HIGH_EXPOSURE = 8
# "9. Travel in the same environment (bus/train/Flight) but not having a high-risk exposure as cited above."
TRAVELLED_TOGETHER_WITHOUT_HIGH_EXPOSURE = 9


# Patient Status cosntants
HOME_ISOLATION = "home-isolation"
RECOVERED = "recovered"
DEAD = "dead"
FACILITY_STATUS = "facility-status"

# Paitient status Choices
PATIENT_STATUS_CHOICES = (
    (HOME_ISOLATION, "Home Isolation"),
    (RECOVERED, "Recovered"),
    (DEAD, "Dead"),
    (FACILITY_STATUS, "Facility Status"),
)

# Patient Transfer Constants
TRANSFER_STATUS = namedtuple("TRANSFER_STATUS", ["PENDING", "ACCEPTED", "REJECTED", "WITHDRAW"])(
    PENDING=1, ACCEPTED=2, REJECTED=3, WITHDRAW=4
)

TRANSFER_STATUS_CHOICES = (
    (TRANSFER_STATUS.PENDING, "Pending"),
    (TRANSFER_STATUS.ACCEPTED, "Accepted"),
    (TRANSFER_STATUS.REJECTED, "Rejected"),
    (TRANSFER_STATUS.WITHDRAW, "Withdraw"),
)

PATIENT_RELATIVE_TYPE_CHOICES = namedtuple(
    "PATIENT_RELATIVE_CHOICES", ["SELF", "FATHER", "MOTHER", "SIBLING", "SPOUSE", "SON", "DAUGHTER", "FRIEND", "OTHER"]
)(SELF=1, FATHER=2, MOTHER=3, SIBLING=4, SPOUSE=5, SON=6, DAUGHTER=7, FRIEND=8, OTHER=9)

PATIENT_RELATIVE_CHOICES = (
    (PATIENT_RELATIVE_TYPE_CHOICES.SELF, "Self"),
    (PATIENT_RELATIVE_TYPE_CHOICES.FATHER, "Father"),
    (PATIENT_RELATIVE_TYPE_CHOICES.MOTHER, "Mother"),
    (PATIENT_RELATIVE_TYPE_CHOICES.SIBLING, "Sibling"),
    (PATIENT_RELATIVE_TYPE_CHOICES.SPOUSE, "Spouse"),
    (PATIENT_RELATIVE_TYPE_CHOICES.SON, "Son"),
    (PATIENT_RELATIVE_TYPE_CHOICES.DAUGHTER, "Daughter"),
    (PATIENT_RELATIVE_TYPE_CHOICES.FRIEND, "Friend"),
    (PATIENT_RELATIVE_TYPE_CHOICES.OTHER, "Other relative"),
)

NATIVE_COUNTRY_TYPE_CHOICES = namedtuple("type", ["IN", "US", "SK", "JP", "NP", "SL", "MS"])(1, 2, 3, 4, 5, 6, 7)

NATIVE_COUNTRY_CHOICES = [
    (NATIVE_COUNTRY_TYPE_CHOICES.IN, "India"),
    (NATIVE_COUNTRY_TYPE_CHOICES.US, "United States"),
    (NATIVE_COUNTRY_TYPE_CHOICES.SK, "South Korea"),
    (NATIVE_COUNTRY_TYPE_CHOICES.JP, "Japan"),
    (NATIVE_COUNTRY_TYPE_CHOICES.NP, "Nepal"),
    (NATIVE_COUNTRY_TYPE_CHOICES.SL, "Sri Lanka"),
    (NATIVE_COUNTRY_TYPE_CHOICES.MS, "Mauritius"),
]
