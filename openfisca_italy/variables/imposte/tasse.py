# -*- coding: utf-8 -*-

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_italy.entita import *


class income_tax(Variable):
    value_type = float
    entity = Persona
    definition_period = MONTH
    label = u"Imposta sul reddito"
    reference = "https://law.gov.example/income_tax"  # Always use the most official source

    # The formula to compute the income tax for a given person at a given period
    def formula(person, period, parameters):
        return person('reddito_lavoro_dipendente_annuale', period) * parameters(period).tasse.aliquota_IRPEF


class social_security_contribution(Variable):
    value_type = float
    entity = Persona
    definition_period = MONTH
    label = u"Contributo progressivo pagato sui salari per finanziare la previdenza sociale"
    reference = "https://law.gov.example/social_security_contribution"  # Always use the most official source

    def formula(person, period, parameters):
        salary = person('reddito_lavoro_dipendente_annuale', period)

        # The social_security_contribution is computed according to a marginal scale.
        scale = parameters(period).tasse.contributo_sicurezza_sociale

        return scale.calc(salary)


class housing_tax(Variable):
    value_type = float
    entity = Famiglia
    definition_period = YEAR  # This housing tax is defined for a year.
    label = u"Imposta pagata da ogni famiglia proporzionalmente alle dimensioni del suo alloggio"
    reference = "https://law.gov.example/housing_tax"  # Always use the most official source

    def formula(household, period, parameters):
        # The housing tax is defined for a year, but depends on the `accomodation_size` and `housing_occupancy_status` on the first month of the year.
        # Here period is a year. We can get the first month of a year with the following shortcut.
        # To build different periods, see http://openfisca.org/doc/coding-the-legislation/35_periods.html#calculating-dependencies-for-a-specific-period
        january = period.first_month
        accommodation_size = household('accomodation_size', january)
        # `housing_occupancy_status` is an Enum variable
        occupancy_status = household('housing_occupancy_status', january)
        HousingOccupancyStatus = occupancy_status.possible_values  # Get the enum associated with the variable
        # To access an enum element, we use the . notation.
        tenant = (occupancy_status == HousingOccupancyStatus.tenant)
        owner = (occupancy_status == HousingOccupancyStatus.owner)
        # The tax is applied only if the household owns or rents its main residency
        return (owner + tenant) * accommodation_size * 10
