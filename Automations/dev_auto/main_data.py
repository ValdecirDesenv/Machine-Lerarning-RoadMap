import transf_CRM as CRM
import transf_TRD as TRD
from windowMsg import get_date
from transf_OUT import generate_transition_bonus


def main():

    dateProcess = get_date() # Example start date, 
    trd_filtered = TRD.transform_TRD()
    crm_filtered = CRM.transform_CRM()
    generate_transition_bonus(trd_filtered, crm_filtered, dateProcess)


# Check if this script is being run directly as the main module
if __name__ == "__main__":
    main()