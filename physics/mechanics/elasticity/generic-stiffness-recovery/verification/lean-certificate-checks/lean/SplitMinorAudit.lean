import MinorBatch21
import Lean.Util.CollectAxioms
import Lean.Elab.Command

open Lean Elab Command in
run_cmd do
  let expected := #[
    ``ValyuResearch.ElasticityMinorCertificates.certificate_2_19,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_2_32,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_2_58,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_2_92,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_2_98,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_2_101,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_3_68,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_3_135,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_3_198,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_3_210,
    ``ValyuResearch.ElasticityMinorCertificates.certificate_3_213]
  let allowed := #[``propext, ``Classical.choice, ``Quot.sound]
  let env ← getEnv
  for name in expected do
    unless (env.find? name).any ConstantInfo.isTheorem do
      throwError "Missing certificate theorem: {name}"
  let names := env.constants.toList.filterMap fun (name, info) =>
    let owned := match env.getModuleIdxFor? name with
      | some index => (#[`MinorCore, `MinorBatch01, `MinorBatch02, `MinorBatch03, `MinorBatch04, `MinorBatch05, `MinorBatch06, `MinorBatch07, `MinorBatch08, `MinorBatch09, `MinorBatch10, `MinorBatch11, `MinorBatch12, `MinorBatch13, `MinorBatch14, `MinorBatch15, `MinorBatch16, `MinorBatch17, `MinorBatch18, `MinorBatch19, `MinorBatch20, `MinorBatch21]).contains env.header.moduleNames[index.toNat]!
      | none => false
    if info.isTheorem && owned then some name else none
  unless names.length ≥ 300 do
    throwError "Incomplete helper inventory: {names.length}"
  for name in names.toArray.qsort Name.quickLt do
    let axioms ← collectAxioms name
    let unexpected := axioms.filter fun axiomName => !allowed.contains axiomName
    unless unexpected.isEmpty do
      throwError "{name} uses unapproved axioms: {unexpected}"
    logInfo m!"PASS {name}: {axioms}"
  logInfo m!"Audited all {names.length} module theorems and all 11 expected certificates."
