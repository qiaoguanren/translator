from .test_reagents import test_reagents
from .test_step_types import test_correct_step_types
from  .test_properties import test_correct_vessels, test_correct_properties
from .test_info import *
from synthreader.tagging import tag_synthesis
from synthreader.interpreting import extract_actions
from synthreader.finishing import action_list_to_xdl
import pytest

# ACROMELOBINIC_ACID_SI2
@pytest.mark.integration
def test_acromelobinic_acid_si2_reagents():
    test_reagents(ACROMELOBINIC_ACID_SI2_INFO)

@pytest.mark.integration
def test_acromelobinic_acid_si2_step_types():
    test_correct_step_types(ACROMELOBINIC_ACID_SI2_INFO)

@pytest.mark.integration
def test_acromelobinic_acid_si2_vessels():
    test_correct_vessels(ACROMELOBINIC_ACID_SI2_INFO)

@pytest.mark.integration
def test_acromelobinic_acid_si2_properties():
    test_correct_properties(ACROMELOBINIC_ACID_SI2_INFO)

@pytest.mark.fast_integration
def test_acromelobinic_acid_si2():
    tagged_synthesis = tag_synthesis(ACROMELOBINIC_ACID_SI2_INFO["text"])
    test_reagents(ACROMELOBINIC_ACID_SI2_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ACROMELOBINIC_ACID_SI2_INFO, x)
    test_correct_vessels(ACROMELOBINIC_ACID_SI2_INFO, x)
    test_correct_properties(ACROMELOBINIC_ACID_SI2_INFO, x)

# ACROMELOBINIC_ACID_SI3
@pytest.mark.integration
def test_acromelobinic_acid_si3_reagents():
    test_reagents(ACROMELOBINIC_ACID_SI3_INFO)

@pytest.mark.integration
def test_acromelobinic_acid_si3_step_types():
    test_correct_step_types(ACROMELOBINIC_ACID_SI3_INFO)

@pytest.mark.integration
def test_acromelobinic_acid_si3_vessels():
    test_correct_vessels(ACROMELOBINIC_ACID_SI3_INFO)

@pytest.mark.integration
def test_acromelobinic_acid_si3_properties():
    test_correct_properties(ACROMELOBINIC_ACID_SI3_INFO)

@pytest.mark.fast_integration
def test_acromelobinic_acid_si3():
    tagged_synthesis = tag_synthesis(ACROMELOBINIC_ACID_SI3_INFO["text"])
    test_reagents(ACROMELOBINIC_ACID_SI3_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ACROMELOBINIC_ACID_SI3_INFO, x)
    test_correct_vessels(ACROMELOBINIC_ACID_SI3_INFO, x)
    test_correct_properties(ACROMELOBINIC_ACID_SI3_INFO, x)

# ALKYL_FLUOR_STEP1
@pytest.mark.integration
def test_alkyl_fluor_step1_reagents():
    test_reagents(ALKYL_FLUOR_STEP1_INFO)

@pytest.mark.integration
def test_alkyl_fluor_step1_step_types():
    test_correct_step_types(ALKYL_FLUOR_STEP1_INFO)

@pytest.mark.integration
def test_alkyl_fluor_step1_vessels():
    test_correct_vessels(ALKYL_FLUOR_STEP1_INFO)

# ALKYL_FLUOR_STEP2
@pytest.mark.integration
def test_alkyl_fluor_step2_reagents():
    test_reagents(ALKYL_FLUOR_STEP2_INFO)

@pytest.mark.integration
def test_alkyl_fluor_step2_step_types():
    test_correct_step_types(ALKYL_FLUOR_STEP2_INFO)

@pytest.mark.integration
def test_alkyl_fluor_step2_vessels():
    test_correct_vessels(ALKYL_FLUOR_STEP2_INFO)

# ALKYL_FLUOR_STEP3
@pytest.mark.integration
def test_alkyl_fluor_step3_reagents():
    test_reagents(ALKYL_FLUOR_STEP3_INFO)

@pytest.mark.integration
def test_alkyl_fluor_step3_step_types():
    test_correct_step_types(ALKYL_FLUOR_STEP3_INFO)

@pytest.mark.integration
def test_alkyl_fluor_step3_vessels():
    test_correct_vessels(ALKYL_FLUOR_STEP3_INFO)

# ALKYL_FLUOR_STEP4
@pytest.mark.integration
def test_alkyl_fluor_step4_reagents():
    test_reagents(ALKYL_FLUOR_STEP4_INFO)

@pytest.mark.integration
def test_alkyl_fluor_step4_step_types():
    test_correct_step_types(ALKYL_FLUOR_STEP4_INFO)

@pytest.mark.integration
def test_alkyl_fluor_step4_vessels():
    test_correct_vessels(ALKYL_FLUOR_STEP4_INFO)

# ALKYL_FLUOR_STEPS_1_3
@pytest.mark.integration
def test_alkyl_fluor_steps_1_3_reagents():
    test_reagents(ALKYL_FLUOR_STEPS_1_3_INFO)

@pytest.mark.integration
def test_alkyl_fluor_steps_1_3_step_types():
    test_correct_step_types(ALKYL_FLUOR_STEPS_1_3_INFO)

@pytest.mark.integration
def test_alkyl_fluor_steps_1_3_vessels():
    test_correct_vessels(ALKYL_FLUOR_STEPS_1_3_INFO)

# ALKYL_FLUOR_STEPS_1_3_SCALED
@pytest.mark.integration
def test_alkyl_fluor_steps_1_3_scaled_reagents():
    test_reagents(ALKYL_FLUOR_STEPS_1_3_SCALED_INFO)

@pytest.mark.integration
def test_alkyl_fluor_steps_1_3_scaled_step_types():
    test_correct_step_types(ALKYL_FLUOR_STEPS_1_3_SCALED_INFO)

@pytest.mark.integration
def test_alkyl_fluor_steps_1_3_scaled_vessels():
    test_correct_vessels(ALKYL_FLUOR_STEPS_1_3_SCALED_INFO)

@pytest.mark.integration
def test_alkyl_fluor_steps_1_3_scaled_properties():
    test_correct_properties(ALKYL_FLUOR_STEPS_1_3_SCALED_INFO)

@pytest.mark.fast_integration
def test_alkyl_fluor_steps_1_3_scaled():
    tagged_synthesis = tag_synthesis(ALKYL_FLUOR_STEPS_1_3_SCALED_INFO["text"])
    test_reagents(ALKYL_FLUOR_STEPS_1_3_SCALED_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ALKYL_FLUOR_STEPS_1_3_SCALED_INFO, x)
    test_correct_vessels(ALKYL_FLUOR_STEPS_1_3_SCALED_INFO, x)
    test_correct_properties(ALKYL_FLUOR_STEPS_1_3_SCALED_INFO, x)

# CSSP11
@pytest.mark.integration
def test_cssp11_reagents():
    test_reagents(CSSP11_INFO)

@pytest.mark.integration
def test_cssp11_step_types():
    test_correct_step_types(CSSP11_INFO)

@pytest.mark.integration
def test_cssp11_vessels():
    test_correct_vessels(CSSP11_INFO)

@pytest.mark.integration
def test_cssp11_properties():
    test_correct_properties(CSSP11_INFO)

@pytest.mark.fast_integration
def test_cssp11():
    tagged_synthesis = tag_synthesis(CSSP11_INFO["text"])
    test_reagents(CSSP11_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP11_INFO, x)
    test_correct_vessels(CSSP11_INFO, x)
    test_correct_properties(CSSP11_INFO, x)

# CSSP12
@pytest.mark.integration
def test_cssp12_reagents():
    test_reagents(CSSP12_INFO)

@pytest.mark.integration
def test_cssp12_step_types():
    test_correct_step_types(CSSP12_INFO)

@pytest.mark.integration
def test_cssp12_vessels():
    test_correct_vessels(CSSP12_INFO)

@pytest.mark.integration
def test_cssp12_properties():
    test_correct_properties(CSSP12_INFO)

@pytest.mark.fast_integration
def test_cssp12():
    tagged_synthesis = tag_synthesis(CSSP12_INFO["text"])
    test_reagents(CSSP12_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP12_INFO, x)
    test_correct_vessels(CSSP12_INFO, x)
    test_correct_properties(CSSP12_INFO, x)

# CSSP13
@pytest.mark.integration
def test_cssp13_reagents():
    test_reagents(CSSP13_INFO)

@pytest.mark.integration
def test_cssp13_step_types():
    test_correct_step_types(CSSP13_INFO)

@pytest.mark.integration
def test_cssp13_vessels():
    test_correct_vessels(CSSP13_INFO)

@pytest.mark.integration
def test_cssp13_properties():
    test_correct_properties(CSSP13_INFO)

@pytest.mark.fast_integration
def test_cssp13():
    tagged_synthesis = tag_synthesis(CSSP13_INFO["text"])
    test_reagents(CSSP13_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP13_INFO, x)
    test_correct_vessels(CSSP13_INFO, x)
    test_correct_properties(CSSP13_INFO, x)

# CSSP16
@pytest.mark.integration
def test_cssp16_reagents():
    test_reagents(CSSP16_INFO)

@pytest.mark.integration
def test_cssp16_step_types():
    test_correct_step_types(CSSP16_INFO)

@pytest.mark.integration
def test_cssp16_vessels():
    test_correct_vessels(CSSP16_INFO)

@pytest.mark.integration
def test_cssp16_properties():
    test_correct_properties(CSSP16_INFO)

@pytest.mark.fast_integration
def test_cssp16():
    tagged_synthesis = tag_synthesis(CSSP16_INFO["text"])
    test_reagents(CSSP16_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP16_INFO, x)
    test_correct_vessels(CSSP16_INFO, x)
    test_correct_properties(CSSP16_INFO, x)

# CSSP17
@pytest.mark.integration
def test_cssp17_reagents():
    test_reagents(CSSP17_INFO)

@pytest.mark.integration
def test_cssp17_step_types():
    test_correct_step_types(CSSP17_INFO)

@pytest.mark.integration
def test_cssp17_vessels():
    test_correct_vessels(CSSP17_INFO)

@pytest.mark.integration
def test_cssp17_properties():
    test_correct_properties(CSSP17_INFO)

@pytest.mark.fast_integration
def test_cssp17():
    tagged_synthesis = tag_synthesis(CSSP17_INFO["text"])
    test_reagents(CSSP17_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP17_INFO, x)
    test_correct_vessels(CSSP17_INFO, x)
    test_correct_properties(CSSP17_INFO, x)

# CSSP18
@pytest.mark.integration
def test_cssp18_reagents():
    test_reagents(CSSP18_INFO)

@pytest.mark.integration
def test_cssp18_step_types():
    test_correct_step_types(CSSP18_INFO)

@pytest.mark.integration
def test_cssp18_vessels():
    test_correct_vessels(CSSP18_INFO)

@pytest.mark.integration
def test_cssp18_properties():
    test_correct_properties(CSSP18_INFO)

@pytest.mark.fast_integration
def test_cssp18():
    tagged_synthesis = tag_synthesis(CSSP18_INFO["text"])
    test_reagents(CSSP18_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP18_INFO, x)
    test_correct_vessels(CSSP18_INFO, x)
    test_correct_properties(CSSP18_INFO, x)

# CSSP1
@pytest.mark.integration
def test_cssp1_reagents():
    test_reagents(CSSP1_INFO)

@pytest.mark.integration
def test_cssp1_step_types():
    test_correct_step_types(CSSP1_INFO)

@pytest.mark.integration
def test_cssp1_vessels():
    test_correct_vessels(CSSP1_INFO)

@pytest.mark.integration
def test_cssp1_properties():
    test_correct_properties(CSSP1_INFO)

@pytest.mark.fast_integration
def test_cssp1():
    tagged_synthesis = tag_synthesis(CSSP1_INFO["text"])
    test_reagents(CSSP1_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP1_INFO, x)
    test_correct_vessels(CSSP1_INFO, x)
    test_correct_properties(CSSP1_INFO, x)

# CSSP20
@pytest.mark.integration
def test_cssp20_reagents():
    test_reagents(CSSP20_INFO)

@pytest.mark.integration
def test_cssp20_step_types():
    test_correct_step_types(CSSP20_INFO)

@pytest.mark.integration
def test_cssp20_vessels():
    test_correct_vessels(CSSP20_INFO)

@pytest.mark.integration
def test_cssp20_properties():
    test_correct_properties(CSSP20_INFO)

@pytest.mark.fast_integration
def test_cssp20():
    tagged_synthesis = tag_synthesis(CSSP20_INFO["text"])
    test_reagents(CSSP20_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP20_INFO, x)
    test_correct_vessels(CSSP20_INFO, x)
    test_correct_properties(CSSP20_INFO, x)

# CSSP21
@pytest.mark.integration
def test_cssp21_reagents():
    test_reagents(CSSP21_INFO)

@pytest.mark.integration
def test_cssp21_step_types():
    test_correct_step_types(CSSP21_INFO)

@pytest.mark.integration
def test_cssp21_vessels():
    test_correct_vessels(CSSP21_INFO)

@pytest.mark.integration
def test_cssp21_properties():
    test_correct_properties(CSSP21_INFO)

@pytest.mark.fast_integration
def test_cssp21():
    tagged_synthesis = tag_synthesis(CSSP21_INFO["text"])
    test_reagents(CSSP21_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP21_INFO, x)
    test_correct_vessels(CSSP21_INFO, x)
    test_correct_properties(CSSP21_INFO, x)

# CSSP22
@pytest.mark.integration
def test_cssp22_reagents():
    test_reagents(CSSP22_INFO)

@pytest.mark.integration
def test_cssp22_step_types():
    test_correct_step_types(CSSP22_INFO)

@pytest.mark.integration
def test_cssp22_vessels():
    test_correct_vessels(CSSP22_INFO)

@pytest.mark.integration
def test_cssp22_properties():
    test_correct_properties(CSSP22_INFO)

@pytest.mark.fast_integration
def test_cssp22():
    tagged_synthesis = tag_synthesis(CSSP22_INFO["text"])
    test_reagents(CSSP22_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP22_INFO, x)
    test_correct_vessels(CSSP22_INFO, x)
    test_correct_properties(CSSP22_INFO, x)

# CSSP23
@pytest.mark.integration
def test_cssp23_reagents():
    test_reagents(CSSP23_INFO)

@pytest.mark.integration
def test_cssp23_step_types():
    test_correct_step_types(CSSP23_INFO)

@pytest.mark.integration
def test_cssp23_vessels():
    test_correct_vessels(CSSP23_INFO)

@pytest.mark.integration
def test_cssp23_properties():
    test_correct_properties(CSSP23_INFO)

@pytest.mark.fast_integration
def test_cssp23():
    tagged_synthesis = tag_synthesis(CSSP23_INFO["text"])
    test_reagents(CSSP23_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP23_INFO, x)
    test_correct_vessels(CSSP23_INFO, x)
    test_correct_properties(CSSP23_INFO, x)

# CSSP24
@pytest.mark.integration
def test_cssp24_reagents():
    test_reagents(CSSP24_INFO)

@pytest.mark.integration
def test_cssp24_step_types():
    test_correct_step_types(CSSP24_INFO)

@pytest.mark.integration
def test_cssp24_vessels():
    test_correct_vessels(CSSP24_INFO)

@pytest.mark.integration
def test_cssp24_properties():
    test_correct_properties(CSSP24_INFO)

@pytest.mark.fast_integration
def test_cssp24():
    tagged_synthesis = tag_synthesis(CSSP24_INFO["text"])
    test_reagents(CSSP24_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP24_INFO, x)
    test_correct_vessels(CSSP24_INFO, x)
    test_correct_properties(CSSP24_INFO, x)

# CSSP25
@pytest.mark.integration
def test_cssp25_reagents():
    test_reagents(CSSP25_INFO)

@pytest.mark.integration
def test_cssp25_step_types():
    test_correct_step_types(CSSP25_INFO)

@pytest.mark.integration
def test_cssp25_vessels():
    test_correct_vessels(CSSP25_INFO)

@pytest.mark.integration
def test_cssp25_properties():
    test_correct_properties(CSSP25_INFO)

@pytest.mark.fast_integration
def test_cssp25():
    tagged_synthesis = tag_synthesis(CSSP25_INFO["text"])
    test_reagents(CSSP25_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP25_INFO, x)
    test_correct_vessels(CSSP25_INFO, x)
    test_correct_properties(CSSP25_INFO, x)

# CSSP2
@pytest.mark.integration
def test_cssp2_reagents():
    test_reagents(CSSP2_INFO)

@pytest.mark.integration
def test_cssp2_step_types():
    test_correct_step_types(CSSP2_INFO)

@pytest.mark.integration
def test_cssp2_vessels():
    test_correct_vessels(CSSP2_INFO)

@pytest.mark.integration
def test_cssp2_properties():
    test_correct_properties(CSSP2_INFO)

@pytest.mark.fast_integration
def test_cssp2():
    tagged_synthesis = tag_synthesis(CSSP2_INFO["text"])
    test_reagents(CSSP2_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP2_INFO, x)
    test_correct_vessels(CSSP2_INFO, x)
    test_correct_properties(CSSP2_INFO, x)

# CSSP4
@pytest.mark.integration
def test_cssp4_reagents():
    test_reagents(CSSP4_INFO)

@pytest.mark.integration
def test_cssp4_step_types():
    test_correct_step_types(CSSP4_INFO)

@pytest.mark.integration
def test_cssp4_vessels():
    test_correct_vessels(CSSP4_INFO)

@pytest.mark.integration
def test_cssp4_properties():
    test_correct_properties(CSSP4_INFO)

@pytest.mark.fast_integration
def test_cssp4():
    tagged_synthesis = tag_synthesis(CSSP4_INFO["text"])
    test_reagents(CSSP4_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP4_INFO, x)
    test_correct_vessels(CSSP4_INFO, x)
    test_correct_properties(CSSP4_INFO, x)

# CSSP5
@pytest.mark.integration
def test_cssp5_reagents():
    test_reagents(CSSP5_INFO)

@pytest.mark.integration
def test_cssp5_step_types():
    test_correct_step_types(CSSP5_INFO)

@pytest.mark.integration
def test_cssp5_vessels():
    test_correct_vessels(CSSP5_INFO)

@pytest.mark.integration
def test_cssp5_properties():
    test_correct_properties(CSSP5_INFO)

@pytest.mark.fast_integration
def test_cssp5():
    tagged_synthesis = tag_synthesis(CSSP5_INFO["text"])
    test_reagents(CSSP5_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP5_INFO, x)
    test_correct_vessels(CSSP5_INFO, x)
    test_correct_properties(CSSP5_INFO, x)

# CSSP6
@pytest.mark.integration
def test_cssp6_reagents():
    test_reagents(CSSP6_INFO)

@pytest.mark.integration
def test_cssp6_step_types():
    test_correct_step_types(CSSP6_INFO)

@pytest.mark.integration
def test_cssp6_vessels():
    test_correct_vessels(CSSP6_INFO)

@pytest.mark.integration
def test_cssp6_properties():
    test_correct_properties(CSSP6_INFO)

@pytest.mark.fast_integration
def test_cssp6():
    tagged_synthesis = tag_synthesis(CSSP6_INFO["text"])
    test_reagents(CSSP6_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP6_INFO, x)
    test_correct_vessels(CSSP6_INFO, x)
    test_correct_properties(CSSP6_INFO, x)

# CSSP8
@pytest.mark.integration
def test_cssp8_reagents():
    test_reagents(CSSP8_INFO)

@pytest.mark.integration
def test_cssp8_step_types():
    test_correct_step_types(CSSP8_INFO)

@pytest.mark.integration
def test_cssp8_vessels():
    test_correct_vessels(CSSP8_INFO)

@pytest.mark.integration
def test_cssp8_properties():
    test_correct_properties(CSSP8_INFO)

@pytest.mark.fast_integration
def test_cssp8():
    tagged_synthesis = tag_synthesis(CSSP8_INFO["text"])
    test_reagents(CSSP8_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(CSSP8_INFO, x)
    test_correct_vessels(CSSP8_INFO, x)
    test_correct_properties(CSSP8_INFO, x)

# DIAZIRINE
@pytest.mark.integration
def test_diazirine_reagents():
    test_reagents(DIAZIRINE_INFO)

@pytest.mark.integration
def test_diazirine_step_types():
    test_correct_step_types(DIAZIRINE_INFO)

@pytest.mark.integration
def test_diazirine_vessels():
    test_correct_vessels(DIAZIRINE_INFO)

@pytest.mark.integration
def test_diazirine_properties():
    test_correct_properties(DIAZIRINE_INFO)

@pytest.mark.fast_integration
def test_diazirine():
    tagged_synthesis = tag_synthesis(DIAZIRINE_INFO["text"])
    test_reagents(DIAZIRINE_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(DIAZIRINE_INFO, x)
    test_correct_vessels(DIAZIRINE_INFO, x)
    test_correct_properties(DIAZIRINE_INFO, x)

# DMERYTH_STEP1
@pytest.mark.integration
def test_dmeryth_step1_reagents():
    test_reagents(DMERYTH_STEP1_INFO)

@pytest.mark.integration
def test_dmeryth_step1_step_types():
    test_correct_step_types(DMERYTH_STEP1_INFO)

@pytest.mark.integration
def test_dmeryth_step1_vessels():
    test_correct_vessels(DMERYTH_STEP1_INFO)

@pytest.mark.integration
def test_dmeryth_step1_properties():
    test_correct_properties(DMERYTH_STEP1_INFO)

@pytest.mark.fast_integration
def test_dmeryth_step1():
    tagged_synthesis = tag_synthesis(DMERYTH_STEP1_INFO["text"])
    test_reagents(DMERYTH_STEP1_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(DMERYTH_STEP1_INFO, x)
    test_correct_vessels(DMERYTH_STEP1_INFO, x)
    test_correct_properties(DMERYTH_STEP1_INFO, x)

# DMERYTH_STEP2
@pytest.mark.integration
def test_dmeryth_step2_reagents():
    test_reagents(DMERYTH_STEP2_INFO)

@pytest.mark.integration
def test_dmeryth_step2_step_types():
    test_correct_step_types(DMERYTH_STEP2_INFO)

@pytest.mark.integration
def test_dmeryth_step2_vessels():
    test_correct_vessels(DMERYTH_STEP2_INFO)

@pytest.mark.integration
def test_dmeryth_step2_properties():
    test_correct_properties(DMERYTH_STEP2_INFO)

@pytest.mark.fast_integration
def test_dmeryth_step2():
    tagged_synthesis = tag_synthesis(DMERYTH_STEP2_INFO["text"])
    test_reagents(DMERYTH_STEP2_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(DMERYTH_STEP2_INFO, x)
    test_correct_vessels(DMERYTH_STEP2_INFO, x)
    test_correct_properties(DMERYTH_STEP2_INFO, x)

# DMP_FULL
@pytest.mark.integration
def test_dmp_full_reagents():
    test_reagents(DMP_FULL_INFO)

@pytest.mark.integration
def test_dmp_full_step_types():
    test_correct_step_types(DMP_FULL_INFO)

@pytest.mark.integration
def test_dmp_full_vessels():
    test_correct_vessels(DMP_FULL_INFO)

@pytest.mark.integration
def test_dmp_full_properties():
    test_correct_properties(DMP_FULL_INFO)

@pytest.mark.fast_integration
def test_dmp_full():
    tagged_synthesis = tag_synthesis(DMP_FULL_INFO["text"])
    test_reagents(DMP_FULL_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(DMP_FULL_INFO, x)
    test_correct_vessels(DMP_FULL_INFO, x)
    test_correct_properties(DMP_FULL_INFO, x)

# DMP_STEP1
@pytest.mark.integration
def test_dmp_step1_reagents():
    test_reagents(DMP_STEP1_INFO)

@pytest.mark.integration
def test_dmp_step1_step_types():
    test_correct_step_types(DMP_STEP1_INFO)

@pytest.mark.integration
def test_dmp_step1_vessels():
    test_correct_vessels(DMP_STEP1_INFO)

# DMP_STEP2
@pytest.mark.integration
def test_dmp_step2_reagents():
    test_reagents(DMP_STEP2_INFO)

@pytest.mark.integration
def test_dmp_step2_step_types():
    test_correct_step_types(DMP_STEP2_INFO)

@pytest.mark.integration
def test_dmp_step2_vessels():
    test_correct_vessels(DMP_STEP2_INFO)

# DMP_STEP3
@pytest.mark.integration
def test_dmp_step3_reagents():
    test_reagents(DMP_STEP3_INFO)

@pytest.mark.integration
def test_dmp_step3_step_types():
    test_correct_step_types(DMP_STEP3_INFO)

@pytest.mark.integration
def test_dmp_step3_vessels():
    test_correct_vessels(DMP_STEP3_INFO)

# EPILUPININE_5A
@pytest.mark.integration
def test_epilupinine_5a_reagents():
    test_reagents(EPILUPININE_5A_INFO)

@pytest.mark.integration
def test_epilupinine_5a_step_types():
    test_correct_step_types(EPILUPININE_5A_INFO)

@pytest.mark.integration
def test_epilupinine_5a_vessels():
    test_correct_vessels(EPILUPININE_5A_INFO)

@pytest.mark.integration
def test_epilupinine_5a_properties():
    test_correct_properties(EPILUPININE_5A_INFO)

@pytest.mark.fast_integration
def test_epilupinine_5a():
    tagged_synthesis = tag_synthesis(EPILUPININE_5A_INFO["text"])
    test_reagents(EPILUPININE_5A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(EPILUPININE_5A_INFO, x)
    test_correct_vessels(EPILUPININE_5A_INFO, x)
    test_correct_properties(EPILUPININE_5A_INFO, x)

# LIDOCAINE
@pytest.mark.integration
def test_lidocaine_reagents():
    test_reagents(LIDOCAINE_INFO)

@pytest.mark.integration
def test_lidocaine_step_types():
    test_correct_step_types(LIDOCAINE_INFO)

@pytest.mark.integration
def test_lidocaine_vessels():
    test_correct_vessels(LIDOCAINE_INFO)

@pytest.mark.integration
def test_lidocaine_properties():
    test_correct_properties(LIDOCAINE_INFO)

@pytest.mark.fast_integration
def test_lidocaine():
    tagged_synthesis = tag_synthesis(LIDOCAINE_INFO["text"])
    test_reagents(LIDOCAINE_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(LIDOCAINE_INFO, x)
    test_correct_vessels(LIDOCAINE_INFO, x)
    test_correct_properties(LIDOCAINE_INFO, x)

# ORGSYN_CV1P0001_ACETAL
@pytest.mark.integration
def test_orgsyn_cv1p0001_acetal_reagents():
    test_reagents(ORGSYN_CV1P0001_ACETAL_INFO)

@pytest.mark.integration
def test_orgsyn_cv1p0001_acetal_step_types():
    test_correct_step_types(ORGSYN_CV1P0001_ACETAL_INFO)

@pytest.mark.integration
def test_orgsyn_cv1p0001_acetal_vessels():
    test_correct_vessels(ORGSYN_CV1P0001_ACETAL_INFO)

@pytest.mark.integration
def test_orgsyn_cv1p0001_acetal_properties():
    test_correct_properties(ORGSYN_CV1P0001_ACETAL_INFO)

@pytest.mark.fast_integration
def test_orgsyn_cv1p0001_acetal():
    tagged_synthesis = tag_synthesis(ORGSYN_CV1P0001_ACETAL_INFO["text"])
    test_reagents(ORGSYN_CV1P0001_ACETAL_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_CV1P0001_ACETAL_INFO, x)
    test_correct_vessels(ORGSYN_CV1P0001_ACETAL_INFO, x)
    test_correct_properties(ORGSYN_CV1P0001_ACETAL_INFO, x)

# ORGSYN_CV1P0058_ANISOLE
@pytest.mark.integration
def test_orgsyn_cv1p0058_anisole_reagents():
    test_reagents(ORGSYN_CV1P0058_ANISOLE_INFO)

@pytest.mark.integration
def test_orgsyn_cv1p0058_anisole_step_types():
    test_correct_step_types(ORGSYN_CV1P0058_ANISOLE_INFO)

@pytest.mark.integration
def test_orgsyn_cv1p0058_anisole_vessels():
    test_correct_vessels(ORGSYN_CV1P0058_ANISOLE_INFO)

@pytest.mark.integration
def test_orgsyn_cv1p0058_anisole_properties():
    test_correct_properties(ORGSYN_CV1P0058_ANISOLE_INFO)

@pytest.mark.fast_integration
def test_orgsyn_cv1p0058_anisole():
    tagged_synthesis = tag_synthesis(ORGSYN_CV1P0058_ANISOLE_INFO["text"])
    test_reagents(ORGSYN_CV1P0058_ANISOLE_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_CV1P0058_ANISOLE_INFO, x)
    test_correct_vessels(ORGSYN_CV1P0058_ANISOLE_INFO, x)
    test_correct_properties(ORGSYN_CV1P0058_ANISOLE_INFO, x)

# ORGSYN_CV9P0001
@pytest.mark.integration
def test_orgsyn_cv9p0001_reagents():
    test_reagents(ORGSYN_CV9P0001_INFO)

@pytest.mark.integration
def test_orgsyn_cv9p0001_step_types():
    test_correct_step_types(ORGSYN_CV9P0001_INFO)

@pytest.mark.integration
def test_orgsyn_cv9p0001_vessels():
    test_correct_vessels(ORGSYN_CV9P0001_INFO)

@pytest.mark.integration
def test_orgsyn_cv9p0001_properties():
    test_correct_properties(ORGSYN_CV9P0001_INFO)

@pytest.mark.fast_integration
def test_orgsyn_cv9p0001():
    tagged_synthesis = tag_synthesis(ORGSYN_CV9P0001_INFO["text"])
    test_reagents(ORGSYN_CV9P0001_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_CV9P0001_INFO, x)
    test_correct_vessels(ORGSYN_CV9P0001_INFO, x)
    test_correct_properties(ORGSYN_CV9P0001_INFO, x)

# ORGSYN_CV9P0004_A
@pytest.mark.integration
def test_orgsyn_cv9p0004_a_reagents():
    test_reagents(ORGSYN_CV9P0004_A_INFO)

@pytest.mark.integration
def test_orgsyn_cv9p0004_a_step_types():
    test_correct_step_types(ORGSYN_CV9P0004_A_INFO)

@pytest.mark.integration
def test_orgsyn_cv9p0004_a_vessels():
    test_correct_vessels(ORGSYN_CV9P0004_A_INFO)

@pytest.mark.integration
def test_orgsyn_cv9p0004_a_properties():
    test_correct_properties(ORGSYN_CV9P0004_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_cv9p0004_a():
    tagged_synthesis = tag_synthesis(ORGSYN_CV9P0004_A_INFO["text"])
    test_reagents(ORGSYN_CV9P0004_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_CV9P0004_A_INFO, x)
    test_correct_vessels(ORGSYN_CV9P0004_A_INFO, x)
    test_correct_properties(ORGSYN_CV9P0004_A_INFO, x)

# ORGSYN_V80P0129
@pytest.mark.integration
def test_orgsyn_v80p0129_reagents():
    test_reagents(ORGSYN_V80P0129_INFO)

@pytest.mark.integration
def test_orgsyn_v80p0129_step_types():
    test_correct_step_types(ORGSYN_V80P0129_INFO)

@pytest.mark.integration
def test_orgsyn_v80p0129_vessels():
    test_correct_vessels(ORGSYN_V80P0129_INFO)

@pytest.mark.integration
def test_orgsyn_v80p0129_properties():
    test_correct_properties(ORGSYN_V80P0129_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v80p0129():
    tagged_synthesis = tag_synthesis(ORGSYN_V80P0129_INFO["text"])
    test_reagents(ORGSYN_V80P0129_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V80P0129_INFO, x)
    test_correct_vessels(ORGSYN_V80P0129_INFO, x)
    test_correct_properties(ORGSYN_V80P0129_INFO, x)

# ORGSYN_V81P0262
@pytest.mark.integration
def test_orgsyn_v81p0262_reagents():
    test_reagents(ORGSYN_V81P0262_INFO)

@pytest.mark.integration
def test_orgsyn_v81p0262_step_types():
    test_correct_step_types(ORGSYN_V81P0262_INFO)

@pytest.mark.integration
def test_orgsyn_v81p0262_vessels():
    test_correct_vessels(ORGSYN_V81P0262_INFO)

@pytest.mark.integration
def test_orgsyn_v81p0262_properties():
    test_correct_properties(ORGSYN_V81P0262_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v81p0262():
    tagged_synthesis = tag_synthesis(ORGSYN_V81P0262_INFO["text"])
    test_reagents(ORGSYN_V81P0262_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V81P0262_INFO, x)
    test_correct_vessels(ORGSYN_V81P0262_INFO, x)
    test_correct_properties(ORGSYN_V81P0262_INFO, x)

# ORGSYN_V82P0059
@pytest.mark.integration
def test_orgsyn_v82p0059_reagents():
    test_reagents(ORGSYN_V82P0059_INFO)

@pytest.mark.integration
def test_orgsyn_v82p0059_step_types():
    test_correct_step_types(ORGSYN_V82P0059_INFO)

@pytest.mark.integration
def test_orgsyn_v82p0059_vessels():
    test_correct_vessels(ORGSYN_V82P0059_INFO)

@pytest.mark.integration
def test_orgsyn_v82p0059_properties():
    test_correct_properties(ORGSYN_V82P0059_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v82p0059():
    tagged_synthesis = tag_synthesis(ORGSYN_V82P0059_INFO["text"])
    test_reagents(ORGSYN_V82P0059_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V82P0059_INFO, x)
    test_correct_vessels(ORGSYN_V82P0059_INFO, x)
    test_correct_properties(ORGSYN_V82P0059_INFO, x)

# ORGSYN_V83P0184_A
@pytest.mark.integration
def test_orgsyn_v83p0184_a_reagents():
    test_reagents(ORGSYN_V83P0184_A_INFO)

@pytest.mark.integration
def test_orgsyn_v83p0184_a_step_types():
    test_correct_step_types(ORGSYN_V83P0184_A_INFO)

@pytest.mark.integration
def test_orgsyn_v83p0184_a_vessels():
    test_correct_vessels(ORGSYN_V83P0184_A_INFO)

@pytest.mark.integration
def test_orgsyn_v83p0184_a_properties():
    test_correct_properties(ORGSYN_V83P0184_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v83p0184_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V83P0184_A_INFO["text"])
    test_reagents(ORGSYN_V83P0184_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V83P0184_A_INFO, x)
    test_correct_vessels(ORGSYN_V83P0184_A_INFO, x)
    test_correct_properties(ORGSYN_V83P0184_A_INFO, x)

# ORGSYN_V83P0184_B
@pytest.mark.integration
def test_orgsyn_v83p0184_b_reagents():
    test_reagents(ORGSYN_V83P0184_B_INFO)

@pytest.mark.integration
def test_orgsyn_v83p0184_b_step_types():
    test_correct_step_types(ORGSYN_V83P0184_B_INFO)

@pytest.mark.integration
def test_orgsyn_v83p0184_b_vessels():
    test_correct_vessels(ORGSYN_V83P0184_B_INFO)

@pytest.mark.integration
def test_orgsyn_v83p0184_b_properties():
    test_correct_properties(ORGSYN_V83P0184_B_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v83p0184_b():
    tagged_synthesis = tag_synthesis(ORGSYN_V83P0184_B_INFO["text"])
    test_reagents(ORGSYN_V83P0184_B_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V83P0184_B_INFO, x)
    test_correct_vessels(ORGSYN_V83P0184_B_INFO, x)
    test_correct_properties(ORGSYN_V83P0184_B_INFO, x)

# ORGSYN_V83P0193
@pytest.mark.integration
def test_orgsyn_v83p0193_reagents():
    test_reagents(ORGSYN_V83P0193_INFO)

@pytest.mark.integration
def test_orgsyn_v83p0193_step_types():
    test_correct_step_types(ORGSYN_V83P0193_INFO)

@pytest.mark.integration
def test_orgsyn_v83p0193_vessels():
    test_correct_vessels(ORGSYN_V83P0193_INFO)

@pytest.mark.integration
def test_orgsyn_v83p0193_properties():
    test_correct_properties(ORGSYN_V83P0193_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v83p0193():
    tagged_synthesis = tag_synthesis(ORGSYN_V83P0193_INFO["text"])
    test_reagents(ORGSYN_V83P0193_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V83P0193_INFO, x)
    test_correct_vessels(ORGSYN_V83P0193_INFO, x)
    test_correct_properties(ORGSYN_V83P0193_INFO, x)

# ORGSYN_V87P0016
@pytest.mark.integration
def test_orgsyn_v87p0016_reagents():
    test_reagents(ORGSYN_V87P0016_INFO)

@pytest.mark.integration
def test_orgsyn_v87p0016_step_types():
    test_correct_step_types(ORGSYN_V87P0016_INFO)

@pytest.mark.integration
def test_orgsyn_v87p0016_vessels():
    test_correct_vessels(ORGSYN_V87P0016_INFO)

@pytest.mark.integration
def test_orgsyn_v87p0016_properties():
    test_correct_properties(ORGSYN_V87P0016_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v87p0016():
    tagged_synthesis = tag_synthesis(ORGSYN_V87P0016_INFO["text"])
    test_reagents(ORGSYN_V87P0016_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V87P0016_INFO, x)
    test_correct_vessels(ORGSYN_V87P0016_INFO, x)
    test_correct_properties(ORGSYN_V87P0016_INFO, x)

# ORGSYN_V87P0192
@pytest.mark.integration
def test_orgsyn_v87p0192_reagents():
    test_reagents(ORGSYN_V87P0192_INFO)

@pytest.mark.integration
def test_orgsyn_v87p0192_step_types():
    test_correct_step_types(ORGSYN_V87P0192_INFO)

@pytest.mark.integration
def test_orgsyn_v87p0192_vessels():
    test_correct_vessels(ORGSYN_V87P0192_INFO)

@pytest.mark.integration
def test_orgsyn_v87p0192_properties():
    test_correct_properties(ORGSYN_V87P0192_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v87p0192():
    tagged_synthesis = tag_synthesis(ORGSYN_V87P0192_INFO["text"])
    test_reagents(ORGSYN_V87P0192_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V87P0192_INFO, x)
    test_correct_vessels(ORGSYN_V87P0192_INFO, x)
    test_correct_properties(ORGSYN_V87P0192_INFO, x)

# ORGSYN_V87P0231_A
@pytest.mark.integration
def test_orgsyn_v87p0231_a_reagents():
    test_reagents(ORGSYN_V87P0231_A_INFO)

@pytest.mark.integration
def test_orgsyn_v87p0231_a_step_types():
    test_correct_step_types(ORGSYN_V87P0231_A_INFO)

@pytest.mark.integration
def test_orgsyn_v87p0231_a_vessels():
    test_correct_vessels(ORGSYN_V87P0231_A_INFO)

@pytest.mark.integration
def test_orgsyn_v87p0231_a_properties():
    test_correct_properties(ORGSYN_V87P0231_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v87p0231_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V87P0231_A_INFO["text"])
    test_reagents(ORGSYN_V87P0231_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V87P0231_A_INFO, x)
    test_correct_vessels(ORGSYN_V87P0231_A_INFO, x)
    test_correct_properties(ORGSYN_V87P0231_A_INFO, x)

# ORGSYN_V88P0152_A
@pytest.mark.integration
def test_orgsyn_v88p0152_a_reagents():
    test_reagents(ORGSYN_V88P0152_A_INFO)

@pytest.mark.integration
def test_orgsyn_v88p0152_a_step_types():
    test_correct_step_types(ORGSYN_V88P0152_A_INFO)

@pytest.mark.integration
def test_orgsyn_v88p0152_a_vessels():
    test_correct_vessels(ORGSYN_V88P0152_A_INFO)

@pytest.mark.integration
def test_orgsyn_v88p0152_a_properties():
    test_correct_properties(ORGSYN_V88P0152_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v88p0152_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V88P0152_A_INFO["text"])
    test_reagents(ORGSYN_V88P0152_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V88P0152_A_INFO, x)
    test_correct_vessels(ORGSYN_V88P0152_A_INFO, x)
    test_correct_properties(ORGSYN_V88P0152_A_INFO, x)

# ORGSYN_V90P0251
@pytest.mark.integration
def test_orgsyn_v90p0251_reagents():
    test_reagents(ORGSYN_V90P0251_INFO)

@pytest.mark.integration
def test_orgsyn_v90p0251_step_types():
    test_correct_step_types(ORGSYN_V90P0251_INFO)

@pytest.mark.integration
def test_orgsyn_v90p0251_vessels():
    test_correct_vessels(ORGSYN_V90P0251_INFO)

@pytest.mark.integration
def test_orgsyn_v90p0251_properties():
    test_correct_properties(ORGSYN_V90P0251_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v90p0251():
    tagged_synthesis = tag_synthesis(ORGSYN_V90P0251_INFO["text"])
    test_reagents(ORGSYN_V90P0251_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V90P0251_INFO, x)
    test_correct_vessels(ORGSYN_V90P0251_INFO, x)
    test_correct_properties(ORGSYN_V90P0251_INFO, x)

# ORGSYN_V95P0001_A
@pytest.mark.integration
def test_orgsyn_v95p0001_a_reagents():
    test_reagents(ORGSYN_V95P0001_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0001_a_step_types():
    test_correct_step_types(ORGSYN_V95P0001_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0001_a_vessels():
    test_correct_vessels(ORGSYN_V95P0001_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0001_a_properties():
    test_correct_properties(ORGSYN_V95P0001_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0001_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0001_A_INFO["text"])
    test_reagents(ORGSYN_V95P0001_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0001_A_INFO, x)
    test_correct_vessels(ORGSYN_V95P0001_A_INFO, x)
    test_correct_properties(ORGSYN_V95P0001_A_INFO, x)

# ORGSYN_V95P0001_B
@pytest.mark.integration
def test_orgsyn_v95p0001_b_reagents():
    test_reagents(ORGSYN_V95P0001_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0001_b_step_types():
    test_correct_step_types(ORGSYN_V95P0001_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0001_b_vessels():
    test_correct_vessels(ORGSYN_V95P0001_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0001_b_properties():
    test_correct_properties(ORGSYN_V95P0001_B_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0001_b():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0001_B_INFO["text"])
    test_reagents(ORGSYN_V95P0001_B_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0001_B_INFO, x)
    test_correct_vessels(ORGSYN_V95P0001_B_INFO, x)
    test_correct_properties(ORGSYN_V95P0001_B_INFO, x)

# ORGSYN_V95P0015_A
@pytest.mark.integration
def test_orgsyn_v95p0015_a_reagents():
    test_reagents(ORGSYN_V95P0015_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0015_a_step_types():
    test_correct_step_types(ORGSYN_V95P0015_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0015_a_vessels():
    test_correct_vessels(ORGSYN_V95P0015_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0015_a_properties():
    test_correct_properties(ORGSYN_V95P0015_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0015_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0015_A_INFO["text"])
    test_reagents(ORGSYN_V95P0015_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0015_A_INFO, x)
    test_correct_vessels(ORGSYN_V95P0015_A_INFO, x)
    test_correct_properties(ORGSYN_V95P0015_A_INFO, x)

# ORGSYN_V95P0015_B
@pytest.mark.integration
def test_orgsyn_v95p0015_b_reagents():
    test_reagents(ORGSYN_V95P0015_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0015_b_step_types():
    test_correct_step_types(ORGSYN_V95P0015_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0015_b_vessels():
    test_correct_vessels(ORGSYN_V95P0015_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0015_b_properties():
    test_correct_properties(ORGSYN_V95P0015_B_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0015_b():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0015_B_INFO["text"])
    test_reagents(ORGSYN_V95P0015_B_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0015_B_INFO, x)
    test_correct_vessels(ORGSYN_V95P0015_B_INFO, x)
    test_correct_properties(ORGSYN_V95P0015_B_INFO, x)

# ORGSYN_V95P0029
@pytest.mark.integration
def test_orgsyn_v95p0029_reagents():
    test_reagents(ORGSYN_V95P0029_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0029_step_types():
    test_correct_step_types(ORGSYN_V95P0029_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0029_vessels():
    test_correct_vessels(ORGSYN_V95P0029_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0029_properties():
    test_correct_properties(ORGSYN_V95P0029_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0029():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0029_INFO["text"])
    test_reagents(ORGSYN_V95P0029_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0029_INFO, x)
    test_correct_vessels(ORGSYN_V95P0029_INFO, x)
    test_correct_properties(ORGSYN_V95P0029_INFO, x)

# ORGSYN_V95P0046_A
@pytest.mark.integration
def test_orgsyn_v95p0046_a_reagents():
    test_reagents(ORGSYN_V95P0046_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0046_a_step_types():
    test_correct_step_types(ORGSYN_V95P0046_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0046_a_vessels():
    test_correct_vessels(ORGSYN_V95P0046_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0046_a_properties():
    test_correct_properties(ORGSYN_V95P0046_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0046_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0046_A_INFO["text"])
    test_reagents(ORGSYN_V95P0046_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0046_A_INFO, x)
    test_correct_vessels(ORGSYN_V95P0046_A_INFO, x)
    test_correct_properties(ORGSYN_V95P0046_A_INFO, x)

# ORGSYN_V95P0046_B
@pytest.mark.integration
def test_orgsyn_v95p0046_b_reagents():
    test_reagents(ORGSYN_V95P0046_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0046_b_step_types():
    test_correct_step_types(ORGSYN_V95P0046_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0046_b_vessels():
    test_correct_vessels(ORGSYN_V95P0046_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0046_b_properties():
    test_correct_properties(ORGSYN_V95P0046_B_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0046_b():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0046_B_INFO["text"])
    test_reagents(ORGSYN_V95P0046_B_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0046_B_INFO, x)
    test_correct_vessels(ORGSYN_V95P0046_B_INFO, x)
    test_correct_properties(ORGSYN_V95P0046_B_INFO, x)

# ORGSYN_V95P0060
@pytest.mark.integration
def test_orgsyn_v95p0060_reagents():
    test_reagents(ORGSYN_V95P0060_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0060_step_types():
    test_correct_step_types(ORGSYN_V95P0060_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0060_vessels():
    test_correct_vessels(ORGSYN_V95P0060_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0060_properties():
    test_correct_properties(ORGSYN_V95P0060_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0060():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0060_INFO["text"])
    test_reagents(ORGSYN_V95P0060_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0060_INFO, x)
    test_correct_vessels(ORGSYN_V95P0060_INFO, x)
    test_correct_properties(ORGSYN_V95P0060_INFO, x)

# ORGSYN_V95P0080_A
@pytest.mark.integration
def test_orgsyn_v95p0080_a_reagents():
    test_reagents(ORGSYN_V95P0080_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0080_a_step_types():
    test_correct_step_types(ORGSYN_V95P0080_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0080_a_vessels():
    test_correct_vessels(ORGSYN_V95P0080_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0080_a_properties():
    test_correct_properties(ORGSYN_V95P0080_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0080_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0080_A_INFO["text"])
    test_reagents(ORGSYN_V95P0080_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0080_A_INFO, x)
    test_correct_vessels(ORGSYN_V95P0080_A_INFO, x)
    test_correct_properties(ORGSYN_V95P0080_A_INFO, x)

# ORGSYN_V95P0080_B
@pytest.mark.integration
def test_orgsyn_v95p0080_b_reagents():
    test_reagents(ORGSYN_V95P0080_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0080_b_step_types():
    test_correct_step_types(ORGSYN_V95P0080_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0080_b_vessels():
    test_correct_vessels(ORGSYN_V95P0080_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0080_b_properties():
    test_correct_properties(ORGSYN_V95P0080_B_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0080_b():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0080_B_INFO["text"])
    test_reagents(ORGSYN_V95P0080_B_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0080_B_INFO, x)
    test_correct_vessels(ORGSYN_V95P0080_B_INFO, x)
    test_correct_properties(ORGSYN_V95P0080_B_INFO, x)

# ORGSYN_V95P0080_C
@pytest.mark.integration
def test_orgsyn_v95p0080_c_reagents():
    test_reagents(ORGSYN_V95P0080_C_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0080_c_step_types():
    test_correct_step_types(ORGSYN_V95P0080_C_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0080_c_vessels():
    test_correct_vessels(ORGSYN_V95P0080_C_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0080_c_properties():
    test_correct_properties(ORGSYN_V95P0080_C_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0080_c():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0080_C_INFO["text"])
    test_reagents(ORGSYN_V95P0080_C_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0080_C_INFO, x)
    test_correct_vessels(ORGSYN_V95P0080_C_INFO, x)
    test_correct_properties(ORGSYN_V95P0080_C_INFO, x)

# ORGSYN_V95P0097_A
@pytest.mark.integration
def test_orgsyn_v95p0097_a_reagents():
    test_reagents(ORGSYN_V95P0097_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0097_a_step_types():
    test_correct_step_types(ORGSYN_V95P0097_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0097_a_vessels():
    test_correct_vessels(ORGSYN_V95P0097_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0097_a_properties():
    test_correct_properties(ORGSYN_V95P0097_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0097_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0097_A_INFO["text"])
    test_reagents(ORGSYN_V95P0097_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0097_A_INFO, x)
    test_correct_vessels(ORGSYN_V95P0097_A_INFO, x)
    test_correct_properties(ORGSYN_V95P0097_A_INFO, x)

# ORGSYN_V95P0097_B
@pytest.mark.integration
def test_orgsyn_v95p0097_b_reagents():
    test_reagents(ORGSYN_V95P0097_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0097_b_step_types():
    test_correct_step_types(ORGSYN_V95P0097_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0097_b_vessels():
    test_correct_vessels(ORGSYN_V95P0097_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0097_b_properties():
    test_correct_properties(ORGSYN_V95P0097_B_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0097_b():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0097_B_INFO["text"])
    test_reagents(ORGSYN_V95P0097_B_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0097_B_INFO, x)
    test_correct_vessels(ORGSYN_V95P0097_B_INFO, x)
    test_correct_properties(ORGSYN_V95P0097_B_INFO, x)

# ORGSYN_V95P0112_A
@pytest.mark.integration
def test_orgsyn_v95p0112_a_reagents():
    test_reagents(ORGSYN_V95P0112_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0112_a_step_types():
    test_correct_step_types(ORGSYN_V95P0112_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0112_a_vessels():
    test_correct_vessels(ORGSYN_V95P0112_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0112_a_properties():
    test_correct_properties(ORGSYN_V95P0112_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0112_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0112_A_INFO["text"])
    test_reagents(ORGSYN_V95P0112_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0112_A_INFO, x)
    test_correct_vessels(ORGSYN_V95P0112_A_INFO, x)
    test_correct_properties(ORGSYN_V95P0112_A_INFO, x)

# ORGSYN_V95P0112_B
@pytest.mark.integration
def test_orgsyn_v95p0112_b_reagents():
    test_reagents(ORGSYN_V95P0112_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0112_b_step_types():
    test_correct_step_types(ORGSYN_V95P0112_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0112_b_vessels():
    test_correct_vessels(ORGSYN_V95P0112_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0112_b_properties():
    test_correct_properties(ORGSYN_V95P0112_B_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0112_b():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0112_B_INFO["text"])
    test_reagents(ORGSYN_V95P0112_B_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0112_B_INFO, x)
    test_correct_vessels(ORGSYN_V95P0112_B_INFO, x)
    test_correct_properties(ORGSYN_V95P0112_B_INFO, x)

# ORGSYN_V95P0127_A
@pytest.mark.integration
def test_orgsyn_v95p0127_a_reagents():
    test_reagents(ORGSYN_V95P0127_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0127_a_step_types():
    test_correct_step_types(ORGSYN_V95P0127_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0127_a_vessels():
    test_correct_vessels(ORGSYN_V95P0127_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0127_a_properties():
    test_correct_properties(ORGSYN_V95P0127_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0127_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0127_A_INFO["text"])
    test_reagents(ORGSYN_V95P0127_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0127_A_INFO, x)
    test_correct_vessels(ORGSYN_V95P0127_A_INFO, x)
    test_correct_properties(ORGSYN_V95P0127_A_INFO, x)

# ORGSYN_V95P0127_B
@pytest.mark.integration
def test_orgsyn_v95p0127_b_reagents():
    test_reagents(ORGSYN_V95P0127_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0127_b_step_types():
    test_correct_step_types(ORGSYN_V95P0127_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0127_b_vessels():
    test_correct_vessels(ORGSYN_V95P0127_B_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0127_b_properties():
    test_correct_properties(ORGSYN_V95P0127_B_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0127_b():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0127_B_INFO["text"])
    test_reagents(ORGSYN_V95P0127_B_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0127_B_INFO, x)
    test_correct_vessels(ORGSYN_V95P0127_B_INFO, x)
    test_correct_properties(ORGSYN_V95P0127_B_INFO, x)

# ORGSYN_V95P0127_C
@pytest.mark.integration
def test_orgsyn_v95p0127_c_reagents():
    test_reagents(ORGSYN_V95P0127_C_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0127_c_step_types():
    test_correct_step_types(ORGSYN_V95P0127_C_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0127_c_vessels():
    test_correct_vessels(ORGSYN_V95P0127_C_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0127_c_properties():
    test_correct_properties(ORGSYN_V95P0127_C_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0127_c():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0127_C_INFO["text"])
    test_reagents(ORGSYN_V95P0127_C_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0127_C_INFO, x)
    test_correct_vessels(ORGSYN_V95P0127_C_INFO, x)
    test_correct_properties(ORGSYN_V95P0127_C_INFO, x)

# ORGSYN_V95P0142_A
@pytest.mark.integration
def test_orgsyn_v95p0142_a_reagents():
    test_reagents(ORGSYN_V95P0142_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_a_step_types():
    test_correct_step_types(ORGSYN_V95P0142_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_a_vessels():
    test_correct_vessels(ORGSYN_V95P0142_A_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_a_properties():
    test_correct_properties(ORGSYN_V95P0142_A_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0142_a():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0142_A_INFO["text"])
    test_reagents(ORGSYN_V95P0142_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0142_A_INFO, x)
    test_correct_vessels(ORGSYN_V95P0142_A_INFO, x)
    test_correct_properties(ORGSYN_V95P0142_A_INFO, x)

# ORGSYN_V95P0142_B_PARA1
@pytest.mark.integration
def test_orgsyn_v95p0142_b_para1_reagents():
    test_reagents(ORGSYN_V95P0142_B_PARA1_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_b_para1_step_types():
    test_correct_step_types(ORGSYN_V95P0142_B_PARA1_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_b_para1_vessels():
    test_correct_vessels(ORGSYN_V95P0142_B_PARA1_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_b_para1_properties():
    test_correct_properties(ORGSYN_V95P0142_B_PARA1_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0142_b_para1():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0142_B_PARA1_INFO["text"])
    test_reagents(ORGSYN_V95P0142_B_PARA1_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0142_B_PARA1_INFO, x)
    test_correct_vessels(ORGSYN_V95P0142_B_PARA1_INFO, x)
    test_correct_properties(ORGSYN_V95P0142_B_PARA1_INFO, x)

# ORGSYN_V95P0142_B_PARA2
@pytest.mark.integration
def test_orgsyn_v95p0142_b_para2_reagents():
    test_reagents(ORGSYN_V95P0142_B_PARA2_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_b_para2_step_types():
    test_correct_step_types(ORGSYN_V95P0142_B_PARA2_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_b_para2_vessels():
    test_correct_vessels(ORGSYN_V95P0142_B_PARA2_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_b_para2_properties():
    test_correct_properties(ORGSYN_V95P0142_B_PARA2_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0142_b_para2():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0142_B_PARA2_INFO["text"])
    test_reagents(ORGSYN_V95P0142_B_PARA2_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0142_B_PARA2_INFO, x)
    test_correct_vessels(ORGSYN_V95P0142_B_PARA2_INFO, x)
    test_correct_properties(ORGSYN_V95P0142_B_PARA2_INFO, x)

# ORGSYN_V95P0142_C
@pytest.mark.integration
def test_orgsyn_v95p0142_c_reagents():
    test_reagents(ORGSYN_V95P0142_C_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_c_step_types():
    test_correct_step_types(ORGSYN_V95P0142_C_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_c_vessels():
    test_correct_vessels(ORGSYN_V95P0142_C_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0142_c_properties():
    test_correct_properties(ORGSYN_V95P0142_C_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0142_c():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0142_C_INFO["text"])
    test_reagents(ORGSYN_V95P0142_C_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0142_C_INFO, x)
    test_correct_vessels(ORGSYN_V95P0142_C_INFO, x)
    test_correct_properties(ORGSYN_V95P0142_C_INFO, x)

# ORGSYN_V95P0157_A_PARAS12
@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras12_reagents():
    test_reagents(ORGSYN_V95P0157_A_PARAS12_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras12_step_types():
    test_correct_step_types(ORGSYN_V95P0157_A_PARAS12_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras12_vessels():
    test_correct_vessels(ORGSYN_V95P0157_A_PARAS12_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras12_properties():
    test_correct_properties(ORGSYN_V95P0157_A_PARAS12_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0157_a_paras12():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0157_A_PARAS12_INFO["text"])
    test_reagents(ORGSYN_V95P0157_A_PARAS12_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0157_A_PARAS12_INFO, x)
    test_correct_vessels(ORGSYN_V95P0157_A_PARAS12_INFO, x)
    test_correct_properties(ORGSYN_V95P0157_A_PARAS12_INFO, x)

# ORGSYN_V95P0157_A_PARAS34
@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras34_reagents():
    test_reagents(ORGSYN_V95P0157_A_PARAS34_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras34_step_types():
    test_correct_step_types(ORGSYN_V95P0157_A_PARAS34_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras34_vessels():
    test_correct_vessels(ORGSYN_V95P0157_A_PARAS34_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras34_properties():
    test_correct_properties(ORGSYN_V95P0157_A_PARAS34_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0157_a_paras34():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0157_A_PARAS34_INFO["text"])
    test_reagents(ORGSYN_V95P0157_A_PARAS34_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0157_A_PARAS34_INFO, x)
    test_correct_vessels(ORGSYN_V95P0157_A_PARAS34_INFO, x)
    test_correct_properties(ORGSYN_V95P0157_A_PARAS34_INFO, x)

# ORGSYN_V95P0157_A_PARAS56
@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras56_reagents():
    test_reagents(ORGSYN_V95P0157_A_PARAS56_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras56_step_types():
    test_correct_step_types(ORGSYN_V95P0157_A_PARAS56_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras56_vessels():
    test_correct_vessels(ORGSYN_V95P0157_A_PARAS56_INFO)

@pytest.mark.integration
def test_orgsyn_v95p0157_a_paras56_properties():
    test_correct_properties(ORGSYN_V95P0157_A_PARAS56_INFO)

@pytest.mark.fast_integration
def test_orgsyn_v95p0157_a_paras56():
    tagged_synthesis = tag_synthesis(ORGSYN_V95P0157_A_PARAS56_INFO["text"])
    test_reagents(ORGSYN_V95P0157_A_PARAS56_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(ORGSYN_V95P0157_A_PARAS56_INFO, x)
    test_correct_vessels(ORGSYN_V95P0157_A_PARAS56_INFO, x)
    test_correct_properties(ORGSYN_V95P0157_A_PARAS56_INFO, x)

# THISOQ_4E
@pytest.mark.integration
def test_thisoq_4e_reagents():
    test_reagents(THISOQ_4E_INFO)

@pytest.mark.integration
def test_thisoq_4e_step_types():
    test_correct_step_types(THISOQ_4E_INFO)

@pytest.mark.integration
def test_thisoq_4e_vessels():
    test_correct_vessels(THISOQ_4E_INFO)

@pytest.mark.integration
def test_thisoq_4e_properties():
    test_correct_properties(THISOQ_4E_INFO)

@pytest.mark.fast_integration
def test_thisoq_4e():
    tagged_synthesis = tag_synthesis(THISOQ_4E_INFO["text"])
    test_reagents(THISOQ_4E_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(THISOQ_4E_INFO, x)
    test_correct_vessels(THISOQ_4E_INFO, x)
    test_correct_properties(THISOQ_4E_INFO, x)

# THISOQ_GENPROC_A
@pytest.mark.integration
def test_thisoq_genproc_a_reagents():
    test_reagents(THISOQ_GENPROC_A_INFO)

@pytest.mark.integration
def test_thisoq_genproc_a_step_types():
    test_correct_step_types(THISOQ_GENPROC_A_INFO)

@pytest.mark.integration
def test_thisoq_genproc_a_vessels():
    test_correct_vessels(THISOQ_GENPROC_A_INFO)

@pytest.mark.integration
def test_thisoq_genproc_a_properties():
    test_correct_properties(THISOQ_GENPROC_A_INFO)

@pytest.mark.fast_integration
def test_thisoq_genproc_a():
    tagged_synthesis = tag_synthesis(THISOQ_GENPROC_A_INFO["text"])
    test_reagents(THISOQ_GENPROC_A_INFO, tagged_synthesis)
    action_list = extract_actions(tagged_synthesis)
    x = action_list_to_xdl(action_list)
    test_correct_step_types(THISOQ_GENPROC_A_INFO, x)
    test_correct_vessels(THISOQ_GENPROC_A_INFO, x)
    test_correct_properties(THISOQ_GENPROC_A_INFO, x)
