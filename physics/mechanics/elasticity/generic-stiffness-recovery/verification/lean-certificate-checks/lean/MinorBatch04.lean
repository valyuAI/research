import MinorBatch03

set_option Elab.async false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

noncomputable section
namespace ValyuResearch.ElasticityMinorCertificates

def original_minor_2_70 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5] ![2, 3, 6])

theorem original_minor_2_70_value (w : Fin 8 → ℂ) :
    original_minor_2_70 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 2)) (w 5))) (cadd (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 3)) (w 5))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 4)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 5)) (w 7))) (cadd (cmul (cmul (-8 : ℂ) (w 3)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 3)) (w 4)) (w 5)))) (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 7))) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 5) 2)) (w 7)))))) := by
  unfold original_minor_2_70
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_72 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 6] ![0, 2, 5])

theorem original_minor_2_72_value (w : Fin 8 → ℂ) :
    original_minor_2_72 w =
    (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (4 : ℂ) (w 2)) (w 4)) (w 6))) := by
  unfold original_minor_2_72
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_75 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 6] ![0, 5, 6])

theorem original_minor_2_75_value (w : Fin 8 → ℂ) :
    original_minor_2_75 w =
    (cadd (cmul (cmul (-4 : ℂ) (w 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 6)) (w 7))) := by
  unfold original_minor_2_75
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_76 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 6] ![0, 5, 7])

theorem original_minor_2_76_value (w : Fin 8 → ℂ) :
    original_minor_2_76 w =
    (cadd (cmul (cmul (12 : ℂ) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (4 : ℂ) (w 2)) (w 5)) (w 6)))) := by
  unfold original_minor_2_76
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_82 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 5, 6] ![0, 1, 5])

theorem original_minor_2_82_value (w : Fin 8 → ℂ) :
    original_minor_2_82 w =
    (cadd (cmul (cmul (cmul (-4 : ℂ) (w 0)) (w 6)) (w 7)) (cmul (cmul (cmul (-12 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2))) := by
  unfold original_minor_2_82
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_83 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 5, 6] ![0, 2, 5])

theorem original_minor_2_83_value (w : Fin 8 → ℂ) :
    original_minor_2_83 w =
    (cmul (cmul (cmul (4 : ℂ) (w 2)) (w 5)) (w 6)) := by
  unfold original_minor_2_83
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_86 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 5, 6] ![0, 4, 5])

theorem original_minor_2_86_value (w : Fin 8 → ℂ) :
    original_minor_2_86 w =
    (cadd (cmul (cmul (cmul (-4 : ℂ) (w 0)) (w 6)) (w 7)) (cadd (cmul (cmul (-4 : ℂ) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (-4 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)))) := by
  unfold original_minor_2_86
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_88 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![1, 4, 5] ![0, 1, 5])

theorem original_minor_2_88_value (w : Fin 8 → ℂ) :
    original_minor_2_88 w =
    (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 4)) (w 5)) (cmul (cmul (cmul (-4 : ℂ) (w 2)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 5))) (cadd (cmul (cmul (cmul (cmul (-4 : ℂ) Complex.I) (w 4)) (w 6)) (w 7)) (cmul (cmul (-8 : ℂ) (w 4)) (cpow (w 7) 2))))) := by
  unfold original_minor_2_88
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_92 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![1, 4, 5] ![0, 2, 6])

theorem original_minor_2_92_value (w : Fin 8 → ℂ) :
    original_minor_2_92 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 1)) (w 3)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)))) (cadd (cmul (cmul (cmul (-64 : ℂ) (w 0)) (w 1)) (w 7)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 3) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (64 : ℂ) (w 0)) (w 3)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 4)) (w 5)))) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2)) (cmul (cmul (cmul (64 : ℂ) (w 0)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cadd (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 1) 3)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 1) 2)) (w 3)))) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 1) 2)) (w 6)) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 1) 2)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2))))) (cadd (cadd (cmul (cmul (cmul (24 : ℂ) (w 1)) (w 2)) (w 4)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 3) 2)))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (64 : ℂ) (w 1)) (w 3)) (w 7)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (cpow (w 4) 2))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 4)) (w 5)) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 6) 2)))) (cadd (cmul (cmul (cmul (72 : ℂ) (w 1)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-176 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 3)) (w 4)))) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-80 : ℂ) (w 2)) (w 5)) (w 7)) (cadd (cmul (cmul (-48 : ℂ) (cpow (w 3) 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 3)) (cpow (w 4) 2)))) (cadd (cmul (cmul (cmul (-104 : ℂ) (w 3)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (208 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6))))) (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 4)) (w 5)) (w 7)))) (cadd (cadd (cmul (cmul (-48 : ℂ) (cpow (w 5) 2)) (w 7)) (cmul (cmul (-56 : ℂ) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (224 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (224 : ℂ) (cpow (w 7) 3)))))))) := by
  unfold original_minor_2_92
  simp only [Matrix.det_fin_three]
  minor_ring

def original_minor_2_94 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![1, 4, 5] ![2, 3, 6])

theorem original_minor_2_94_value (w : Fin 8 → ℂ) :
    original_minor_2_94 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (w 3)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)))) (cadd (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 1)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 3) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 3)) (w 7)) (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 4)) (w 5)))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2)) (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 3)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 6)))) (cadd (cmul (cmul (8 : ℂ) (cpow (w 1) 2)) (w 7)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (cmul (cmul (cmul (-24 : ℂ) (w 1)) (w 2)) (w 4))))) (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (cpow (w 3) 2)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 3)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 3)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 4) 2))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 4)) (w 5)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (cpow (w 6) 2))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 1)) (cpow (w 7) 2)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)))) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 7)) (cadd (cmul (cmul (cmul (24 : ℂ) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (cmul (-40 : ℂ) Complex.I) (w 2)) (w 3)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 2)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 5)) (w 7)))) (cadd (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 3) 3)) (cadd (cmul (cmul (cmul (-24 : ℂ) Complex.I) (cpow (w 3) 2)) (w 6)) (cmul (cmul (-24 : ℂ) (cpow (w 3) 2)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 3)) (cpow (w 4) 2)) (cadd (cmul (cmul (cmul (24 : ℂ) (w 3)) (w 4)) (w 5)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 3)) (cpow (w 5) 2)))) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 3)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (-24 : ℂ) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 3)) (cpow (w 7) 2))))) (cadd (cadd (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 5) 2)) (w 6)))) (cadd (cadd (cmul (cmul (40 : ℂ) (cpow (w 5) 2)) (w 7)) (cmul (cmul (16 : ℂ) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 6)) (cpow (w 7) 2)) (cmul (-64 : ℂ) (cpow (w 7) 3)))))))) := by
  unfold original_minor_2_94
  simp only [Matrix.det_fin_three]
  minor_ring

#eval do
  IO.println "Processed rank-2 minor evaluations 70/70"
  (← IO.getStdout).flush

def certificate_2_19_target (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cmul (cmul (cmul (1 : ℂ) (w 2)) (w 5)) (w 7)) (cadd (cmul (cmul (2 : ℂ) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (cmul (-2 : ℂ) Complex.I) (w 4)) (w 5)) (w 7))))

def certificate_2_19_chunk_0 (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cadd (cmul (-3 : ℂ) (original_minor_2_1 w)) (cmul (-9 : ℂ) (original_minor_2_3 w))) (cadd (cmul (3 : ℂ) (original_minor_2_5 w)) (cmul (cmul (-2 : ℂ) Complex.I) (original_minor_2_9 w)))) (cadd (cadd (cmul (-3 : ℂ) (original_minor_2_13 w)) (cmul (-3 : ℂ) (original_minor_2_18 w))) (cadd (cmul (-3 : ℂ) (original_minor_2_20 w)) (cmul (cmul (6 : ℂ) Complex.I) (original_minor_2_33 w))))) (cadd (cadd (cadd (cmul (-6 : ℂ) (original_minor_2_39 w)) (cmul (cmul (6 : ℂ) Complex.I) (original_minor_2_46 w))) (cadd (cmul (cmul (-1 : ℂ) Complex.I) (original_minor_2_58 w)) (cmul (cmul (-3 : ℂ) Complex.I) (original_minor_2_62 w)))) (cadd (cadd (cmul (cmul (-4 : ℂ) Complex.I) (original_minor_2_64 w)) (cmul (-20 : ℂ) (original_minor_2_72 w))) (cadd (cmul (cmul (-16 : ℂ) Complex.I) (original_minor_2_76 w)) (cmul (cmul (6 : ℂ) Complex.I) (original_minor_2_83 w))))))

def certificate_2_19_chunk_0_polynomial (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 5)) (w 7)) (cadd (cmul (cmul (32 : ℂ) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 4)) (w 5)) (w 7))))

theorem certificate_2_19_chunk_0_identity (w : Fin 8 → ℂ) :
    certificate_2_19_chunk_0 w = certificate_2_19_chunk_0_polynomial w := by
  unfold certificate_2_19_chunk_0 certificate_2_19_chunk_0_polynomial
  simp only [original_minor_2_1_value, original_minor_2_3_value, original_minor_2_5_value, original_minor_2_9_value, original_minor_2_13_value, original_minor_2_18_value, original_minor_2_20_value, original_minor_2_33_value, original_minor_2_39_value, original_minor_2_46_value, original_minor_2_58_value, original_minor_2_62_value, original_minor_2_64_value, original_minor_2_72_value, original_minor_2_76_value, original_minor_2_83_value]
  gaussian_ring

#eval do
  IO.println "Processed certificate_2_19_chunk_0"
  (← IO.getStdout).flush

/-- Exact identity in the original minors, with denominators cleared. -/
theorem certificate_2_19 (w : Fin 8 → ℂ) :
    16 * certificate_2_19_target w =
    (certificate_2_19_chunk_0 w) := by
  simp only [certificate_2_19_chunk_0_identity]
  unfold certificate_2_19_target certificate_2_19_chunk_0_polynomial
  try simp only [cadd, cmul, cpow]
  ring

#print axioms certificate_2_19

def certificate_2_32_target (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cmul (1 : ℂ) (cpow (w 6) 3)) (cmul (cmul (cmul (-2 : ℂ) Complex.I) (cpow (w 6) 2)) (w 7)))

def certificate_2_32_chunk_0 (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cadd (cmul (cmul (1 : ℂ) Complex.I) (original_minor_2_1 w)) (cmul (cmul (2 : ℂ) Complex.I) (original_minor_2_3 w))) (cadd (cmul (cmul (-1 : ℂ) Complex.I) (original_minor_2_5 w)) (cmul (2 : ℂ) (original_minor_2_7 w)))) (cadd (cadd (cmul (2 : ℂ) (original_minor_2_9 w)) (cmul (2 : ℂ) (original_minor_2_11 w))) (cadd (cmul (cmul (-2 : ℂ) Complex.I) (original_minor_2_12 w)) (cmul (cmul (1 : ℂ) Complex.I) (original_minor_2_13 w))))) (cadd (cadd (cadd (cmul (cmul (3 : ℂ) Complex.I) (original_minor_2_18 w)) (cmul (cmul (1 : ℂ) Complex.I) (original_minor_2_20 w))) (cadd (cmul (cmul (-1 : ℂ) Complex.I) (original_minor_2_28 w)) (cmul (-6 : ℂ) (original_minor_2_30 w)))) (cadd (cadd (cmul (cmul (-2 : ℂ) Complex.I) (original_minor_2_32 w)) (cmul (-6 : ℂ) (original_minor_2_33 w))) (cadd (cmul (cmul (4 : ℂ) Complex.I) (original_minor_2_35 w)) (cmul (2 : ℂ) (original_minor_2_38 w))))))

def certificate_2_32_chunk_0_polynomial (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (64 : ℂ) (cpow (w 0) 2)) (w 1)) (cmul (cmul (-64 : ℂ) (cpow (w 0) 2)) (w 3))) (cadd (cmul (cmul (-144 : ℂ) (cpow (w 0) 2)) (w 6)) (cmul (cmul (cmul (288 : ℂ) Complex.I) (cpow (w 0) 2)) (w 7)))) (cadd (cadd (cmul (cmul (-32 : ℂ) (w 0)) (cpow (w 1) 2)) (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 1)) (w 3))) (cadd (cmul (cmul (cmul (104 : ℂ) (w 0)) (w 1)) (w 6)) (cadd (cmul (cmul (cmul (cmul (176 : ℂ) Complex.I) (w 0)) (w 1)) (w 7)) (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 3)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-320 : ℂ) Complex.I) (w 0)) (w 3)) (w 7)) (cmul (cmul (-48 : ℂ) (w 0)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (-672 : ℂ) Complex.I) (w 0)) (w 6)) (w 7)) (cadd (cmul (cmul (-1536 : ℂ) (w 0)) (cpow (w 7) 2)) (cmul (cmul (-16 : ℂ) (cpow (w 1) 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (-64 : ℂ) Complex.I) (cpow (w 1) 2)) (w 7)) (cmul (cmul (32 : ℂ) (w 1)) (cpow (w 2) 2))) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (cadd (cmul (cmul (cmul (32 : ℂ) (w 1)) (w 2)) (w 5)) (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 3)) (w 6))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 1)) (w 3)) (w 7)) (cmul (cmul (24 : ℂ) (w 1)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (216 : ℂ) Complex.I) (w 1)) (w 6)) (w 7)) (cmul (cmul (-48 : ℂ) (w 1)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (-32 : ℂ) (cpow (w 2) 2)) (w 3)) (cmul (cmul (-72 : ℂ) (cpow (w 2) 2)) (w 6))) (cadd (cmul (cmul (cmul (144 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (cmul (cmul (cmul (-32 : ℂ) (w 2)) (w 3)) (w 5)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-72 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-144 : ℂ) (w 2)) (w 4)) (w 7))) (cadd (cmul (cmul (cmul (-48 : ℂ) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 3)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (384 : ℂ) (w 3)) (cpow (w 7) 2)) (cmul (8 : ℂ) (cpow (w 6) 3))) (cadd (cmul (cmul (cmul (-192 : ℂ) Complex.I) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (624 : ℂ) (w 6)) (cpow (w 7) 2)) (cmul (cmul (-1952 : ℂ) Complex.I) (cpow (w 7) 3))))))))

theorem certificate_2_32_chunk_0_identity (w : Fin 8 → ℂ) :
    certificate_2_32_chunk_0 w = certificate_2_32_chunk_0_polynomial w := by
  unfold certificate_2_32_chunk_0 certificate_2_32_chunk_0_polynomial
  simp only [original_minor_2_1_value, original_minor_2_3_value, original_minor_2_5_value, original_minor_2_7_value, original_minor_2_9_value, original_minor_2_11_value, original_minor_2_12_value, original_minor_2_13_value, original_minor_2_18_value, original_minor_2_20_value, original_minor_2_28_value, original_minor_2_30_value, original_minor_2_32_value, original_minor_2_33_value, original_minor_2_35_value, original_minor_2_38_value]
  gaussian_ring

#eval do
  IO.println "Processed certificate_2_32_chunk_0"
  (← IO.getStdout).flush

def certificate_2_32_chunk_1 (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cmul (2 : ℂ) (original_minor_2_46 w)) (cmul (cmul (-12 : ℂ) Complex.I) (original_minor_2_51 w))) (cadd (cmul (cmul (-2 : ℂ) Complex.I) (original_minor_2_54 w)) (cmul (cmul (-4 : ℂ) Complex.I) (original_minor_2_56 w)))) (cadd (cadd (cmul (-8 : ℂ) (original_minor_2_57 w)) (cmul (cmul (-2 : ℂ) Complex.I) (original_minor_2_69 w))) (cadd (cmul (cmul (4 : ℂ) Complex.I) (original_minor_2_82 w)) (cmul (cmul (-4 : ℂ) Complex.I) (original_minor_2_86 w)))))

def certificate_2_32_chunk_1_polynomial (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (-64 : ℂ) (cpow (w 0) 2)) (w 1)) (cmul (cmul (64 : ℂ) (cpow (w 0) 2)) (w 3))) (cadd (cmul (cmul (144 : ℂ) (cpow (w 0) 2)) (w 6)) (cmul (cmul (cmul (-288 : ℂ) Complex.I) (cpow (w 0) 2)) (w 7)))) (cadd (cadd (cmul (cmul (32 : ℂ) (w 0)) (cpow (w 1) 2)) (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 1)) (w 3))) (cadd (cmul (cmul (cmul (-104 : ℂ) (w 0)) (w 1)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-176 : ℂ) Complex.I) (w 0)) (w 1)) (w 7)) (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 3)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (320 : ℂ) Complex.I) (w 0)) (w 3)) (w 7)) (cmul (cmul (48 : ℂ) (w 0)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (672 : ℂ) Complex.I) (w 0)) (w 6)) (w 7)) (cmul (cmul (1536 : ℂ) (w 0)) (cpow (w 7) 2)))) (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 1) 2)) (w 6)) (cmul (cmul (cmul (64 : ℂ) Complex.I) (cpow (w 1) 2)) (w 7))) (cadd (cmul (cmul (-32 : ℂ) (w 1)) (cpow (w 2) 2)) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (cmul (cmul (cmul (-32 : ℂ) (w 1)) (w 2)) (w 5))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 3)) (w 6)) (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 1)) (w 3)) (w 7))) (cadd (cmul (cmul (-24 : ℂ) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-216 : ℂ) Complex.I) (w 1)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (48 : ℂ) (w 1)) (cpow (w 7) 2)) (cmul (cmul (32 : ℂ) (cpow (w 2) 2)) (w 3))) (cadd (cmul (cmul (72 : ℂ) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (cmul (-144 : ℂ) Complex.I) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)))))) (cadd (cadd (cadd (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (144 : ℂ) (w 2)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (48 : ℂ) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 2)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 3)) (w 6)) (w 7)) (cmul (cmul (-384 : ℂ) (w 3)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (176 : ℂ) Complex.I) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (-624 : ℂ) (w 6)) (cpow (w 7) 2)) (cmul (cmul (1952 : ℂ) Complex.I) (cpow (w 7) 3))))))))

theorem certificate_2_32_chunk_1_identity (w : Fin 8 → ℂ) :
    certificate_2_32_chunk_1 w = certificate_2_32_chunk_1_polynomial w := by
  unfold certificate_2_32_chunk_1 certificate_2_32_chunk_1_polynomial
  simp only [original_minor_2_46_value, original_minor_2_51_value, original_minor_2_54_value, original_minor_2_56_value, original_minor_2_57_value, original_minor_2_69_value, original_minor_2_82_value, original_minor_2_86_value]
  gaussian_ring

#eval do
  IO.println "Processed certificate_2_32_chunk_1"
  (← IO.getStdout).flush

/-- Exact identity in the original minors, with denominators cleared. -/
theorem certificate_2_32 (w : Fin 8 → ℂ) :
    8 * certificate_2_32_target w =
    (cadd (certificate_2_32_chunk_0 w) (certificate_2_32_chunk_1 w)) := by
  simp only [certificate_2_32_chunk_0_identity, certificate_2_32_chunk_1_identity]
  unfold certificate_2_32_target certificate_2_32_chunk_0_polynomial certificate_2_32_chunk_1_polynomial
  try simp only [cadd, cmul, cpow]
  ring

#print axioms certificate_2_32

def certificate_2_58_target (w : Fin 8 → ℂ) : ℂ :=
    (cmul (1 : ℂ) (cpow (w 5) 3))

def certificate_2_58_chunk_0 (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cadd (cmul (165 : ℂ) (original_minor_2_0 w)) (cmul (cmul (-94 : ℂ) Complex.I) (original_minor_2_2 w))) (cadd (cmul (cmul (139 : ℂ) Complex.I) (original_minor_2_4 w)) (cmul (-25 : ℂ) (original_minor_2_8 w)))) (cadd (cadd (cmul (-4 : ℂ) (original_minor_2_10 w)) (cmul (cmul (66 : ℂ) Complex.I) (original_minor_2_14 w))) (cadd (cmul (cmul (63 : ℂ) Complex.I) (original_minor_2_16 w)) (cmul (103 : ℂ) (original_minor_2_17 w))))) (cadd (cadd (cadd (cmul (cmul (3 : ℂ) Complex.I) (original_minor_2_19 w)) (cmul (-12 : ℂ) (original_minor_2_26 w))) (cadd (cmul (cmul (130 : ℂ) Complex.I) (original_minor_2_31 w)) (cmul (cmul (-8 : ℂ) Complex.I) (original_minor_2_34 w)))) (cadd (cadd (cmul (cmul (-130 : ℂ) Complex.I) (original_minor_2_36 w)) (cmul (-40 : ℂ) (original_minor_2_37 w))) (cadd (cmul (8 : ℂ) (original_minor_2_40 w)) (cmul (-20 : ℂ) (original_minor_2_42 w))))))

def certificate_2_58_chunk_0_polynomial (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (480 : ℂ) (w 0)) (w 1)) (w 2)) (cmul (cmul (cmul (cmul (-960 : ℂ) Complex.I) (w 0)) (w 1)) (w 4))) (cadd (cmul (cmul (cmul (-960 : ℂ) (w 0)) (w 1)) (w 5)) (cadd (cmul (cmul (cmul (-480 : ℂ) (w 0)) (w 2)) (w 3)) (cmul (cmul (cmul (-1344 : ℂ) (w 0)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (2688 : ℂ) Complex.I) (w 0)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (960 : ℂ) Complex.I) (w 0)) (w 3)) (w 4)) (cmul (cmul (cmul (960 : ℂ) (w 0)) (w 3)) (w 5)))) (cadd (cmul (cmul (cmul (cmul (1152 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (2304 : ℂ) (w 0)) (w 4)) (w 7)) (cmul (cmul (cmul (1152 : ℂ) (w 0)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-2304 : ℂ) Complex.I) (w 0)) (w 5)) (w 7)) (cmul (cmul (cmul (480 : ℂ) Complex.I) (cpow (w 1) 2)) (w 4))) (cadd (cmul (cmul (480 : ℂ) (cpow (w 1) 2)) (w 5)) (cadd (cmul (cmul (cmul (480 : ℂ) (w 1)) (w 2)) (w 3)) (cmul (cmul (cmul (480 : ℂ) (w 1)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (480 : ℂ) Complex.I) (w 1)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-480 : ℂ) Complex.I) (w 1)) (w 3)) (w 4)) (cmul (cmul (cmul (-480 : ℂ) (w 1)) (w 3)) (w 5)))) (cadd (cmul (cmul (cmul (cmul (-576 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (1728 : ℂ) (w 1)) (w 4)) (w 7)) (cmul (cmul (cmul (-576 : ℂ) (w 1)) (w 5)) (w 6))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-1728 : ℂ) Complex.I) (w 1)) (w 5)) (w 7)) (cmul (-864 : ℂ) (cpow (w 2) 3))) (cadd (cmul (cmul (cmul (-576 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (cadd (cmul (cmul (-1248 : ℂ) (cpow (w 2) 2)) (w 5)) (cmul (cmul (-480 : ℂ) (w 2)) (cpow (w 3) 2))))) (cadd (cadd (cmul (cmul (cmul (-1056 : ℂ) (w 2)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (672 : ℂ) Complex.I) (w 2)) (w 3)) (w 7)) (cmul (cmul (-864 : ℂ) (w 2)) (cpow (w 4) 2)))) (cadd (cmul (cmul (cmul (cmul (96 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (cadd (cmul (cmul (-288 : ℂ) (w 2)) (cpow (w 5) 2)) (cmul (cmul (-552 : ℂ) (w 2)) (cpow (w 6) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-1824 : ℂ) Complex.I) (w 2)) (w 6)) (w 7)) (cadd (cmul (cmul (-5856 : ℂ) (w 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (-2880 : ℂ) (w 3)) (w 4)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (2880 : ℂ) Complex.I) (w 3)) (w 5)) (w 7)) (cadd (cmul (cmul (-576 : ℂ) Complex.I) (cpow (w 4) 3)) (cmul (cmul (-768 : ℂ) (cpow (w 4) 2)) (w 5))))) (cadd (cadd (cmul (cmul (cmul (288 : ℂ) Complex.I) (w 4)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (-3456 : ℂ) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (6912 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2)))) (cadd (cmul (96 : ℂ) (cpow (w 5) 3)) (cadd (cmul (cmul (cmul (cmul (3456 : ℂ) Complex.I) (w 5)) (w 6)) (w 7)) (cmul (cmul (6912 : ℂ) (w 5)) (cpow (w 7) 2))))))))

theorem certificate_2_58_chunk_0_identity (w : Fin 8 → ℂ) :
    certificate_2_58_chunk_0 w = certificate_2_58_chunk_0_polynomial w := by
  unfold certificate_2_58_chunk_0 certificate_2_58_chunk_0_polynomial
  simp only [original_minor_2_0_value, original_minor_2_2_value, original_minor_2_4_value, original_minor_2_8_value, original_minor_2_10_value, original_minor_2_14_value, original_minor_2_16_value, original_minor_2_17_value, original_minor_2_19_value, original_minor_2_26_value, original_minor_2_31_value, original_minor_2_34_value, original_minor_2_36_value, original_minor_2_37_value, original_minor_2_40_value, original_minor_2_42_value]
  gaussian_ring

#eval do
  IO.println "Processed certificate_2_58_chunk_0"
  (← IO.getStdout).flush

def certificate_2_58_chunk_1 (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cmul (-72 : ℂ) (original_minor_2_44 w)) (cmul (cmul (-36 : ℂ) Complex.I) (original_minor_2_45 w))) (cadd (cmul (90 : ℂ) (original_minor_2_50 w)) (cadd (cmul (6 : ℂ) (original_minor_2_53 w)) (cmul (cmul (-96 : ℂ) Complex.I) (original_minor_2_55 w))))) (cadd (cadd (cmul (-6 : ℂ) (original_minor_2_59 w)) (cadd (cmul (cmul (24 : ℂ) Complex.I) (original_minor_2_65 w)) (cmul (cmul (24 : ℂ) Complex.I) (original_minor_2_67 w)))) (cadd (cmul (-6 : ℂ) (original_minor_2_68 w)) (cadd (cmul (6 : ℂ) (original_minor_2_75 w)) (cmul (cmul (12 : ℂ) Complex.I) (original_minor_2_88 w))))))

def certificate_2_58_chunk_1_polynomial (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-480 : ℂ) (w 0)) (w 1)) (w 2)) (cmul (cmul (cmul (cmul (960 : ℂ) Complex.I) (w 0)) (w 1)) (w 4))) (cadd (cmul (cmul (cmul (960 : ℂ) (w 0)) (w 1)) (w 5)) (cadd (cmul (cmul (cmul (480 : ℂ) (w 0)) (w 2)) (w 3)) (cmul (cmul (cmul (1344 : ℂ) (w 0)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-2688 : ℂ) Complex.I) (w 0)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-960 : ℂ) Complex.I) (w 0)) (w 3)) (w 4)) (cmul (cmul (cmul (-960 : ℂ) (w 0)) (w 3)) (w 5)))) (cadd (cmul (cmul (cmul (cmul (-1152 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (-2304 : ℂ) (w 0)) (w 4)) (w 7)) (cmul (cmul (cmul (-1152 : ℂ) (w 0)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (2304 : ℂ) Complex.I) (w 0)) (w 5)) (w 7)) (cmul (cmul (cmul (-480 : ℂ) Complex.I) (cpow (w 1) 2)) (w 4))) (cadd (cmul (cmul (-480 : ℂ) (cpow (w 1) 2)) (w 5)) (cadd (cmul (cmul (cmul (-480 : ℂ) (w 1)) (w 2)) (w 3)) (cmul (cmul (cmul (-480 : ℂ) (w 1)) (w 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (-480 : ℂ) Complex.I) (w 1)) (w 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (480 : ℂ) Complex.I) (w 1)) (w 3)) (w 4)) (cmul (cmul (cmul (480 : ℂ) (w 1)) (w 3)) (w 5)))) (cadd (cmul (cmul (cmul (cmul (576 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (-1728 : ℂ) (w 1)) (w 4)) (w 7)) (cmul (cmul (cmul (576 : ℂ) (w 1)) (w 5)) (w 6))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (1728 : ℂ) Complex.I) (w 1)) (w 5)) (w 7)) (cmul (864 : ℂ) (cpow (w 2) 3))) (cadd (cmul (cmul (cmul (576 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (cadd (cmul (cmul (1248 : ℂ) (cpow (w 2) 2)) (w 5)) (cmul (cmul (480 : ℂ) (w 2)) (cpow (w 3) 2))))) (cadd (cadd (cmul (cmul (cmul (1056 : ℂ) (w 2)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-672 : ℂ) Complex.I) (w 2)) (w 3)) (w 7)) (cmul (cmul (864 : ℂ) (w 2)) (cpow (w 4) 2)))) (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (cadd (cmul (cmul (288 : ℂ) (w 2)) (cpow (w 5) 2)) (cmul (cmul (552 : ℂ) (w 2)) (cpow (w 6) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (1824 : ℂ) Complex.I) (w 2)) (w 6)) (w 7)) (cmul (cmul (5856 : ℂ) (w 2)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (2880 : ℂ) (w 3)) (w 4)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-2880 : ℂ) Complex.I) (w 3)) (w 5)) (w 7)) (cmul (cmul (576 : ℂ) Complex.I) (cpow (w 4) 3))))) (cadd (cadd (cmul (cmul (768 : ℂ) (cpow (w 4) 2)) (w 5)) (cadd (cmul (cmul (cmul (-288 : ℂ) Complex.I) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (3456 : ℂ) (w 4)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (-6912 : ℂ) Complex.I) (w 4)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-3456 : ℂ) Complex.I) (w 5)) (w 6)) (w 7)) (cmul (cmul (-6912 : ℂ) (w 5)) (cpow (w 7) 2))))))))

theorem certificate_2_58_chunk_1_identity (w : Fin 8 → ℂ) :
    certificate_2_58_chunk_1 w = certificate_2_58_chunk_1_polynomial w := by
  unfold certificate_2_58_chunk_1 certificate_2_58_chunk_1_polynomial
  simp only [original_minor_2_44_value, original_minor_2_45_value, original_minor_2_50_value, original_minor_2_53_value, original_minor_2_55_value, original_minor_2_59_value, original_minor_2_65_value, original_minor_2_67_value, original_minor_2_68_value, original_minor_2_75_value, original_minor_2_88_value]
  gaussian_ring

#eval do
  IO.println "Processed certificate_2_58_chunk_1"
  (← IO.getStdout).flush


end ValyuResearch.ElasticityMinorCertificates
