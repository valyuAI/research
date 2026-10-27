import ValyuResearch
import Lean.Util.CollectAxioms
import Lean.Elab.Command

open Lean Elab Command in
run_cmd do
  let allowed := #[``propext, ``Classical.choice, ``Quot.sound]
  let env ← getEnv
  let names := env.constants.toList.filterMap fun (name, info) =>
    let owned := match env.getModuleIdxFor? name with
      | some index => (`ValyuResearch).isPrefixOf env.header.moduleNames[index.toNat]!
      | none => false
    if info.isTheorem && (owned || (`ValyuResearch).isPrefixOf name) then some name else none
  if names.isEmpty then
    throwError "No project theorems found; refusing an empty audit."
  for name in names.toArray.qsort Name.quickLt do
    let axioms ← collectAxioms name
    let unexpected := axioms.filter fun axiomName => !allowed.contains axiomName
    unless unexpected.isEmpty do
      throwError "{name} uses unapproved axioms: {unexpected}"
    logInfo m!"PASS {name.toString}: {axioms}"
  logInfo m!"Audited {names.length} project theorems; only standard foundational axioms occur."
