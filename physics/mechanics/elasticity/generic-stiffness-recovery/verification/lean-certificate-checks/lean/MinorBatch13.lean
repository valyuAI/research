import MinorBatch12

set_option Elab.async false
set_option maxHeartbeats 8000000
set_option maxRecDepth 4096

noncomputable section
namespace ValyuResearch.ElasticityMinorCertificates

def original_minor_3_184 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 4, 5])

theorem original_minor_3_184_value (w : Fin 8 → ℂ) :
    original_minor_3_184 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 0) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (64 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (cpow (w 6) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) (w 4)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 4)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 5)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) (w 5)) (w 6)) (cpow (w 7) 2))))))) := by
  unfold original_minor_3_184
  simp only [det_fin_four]
  minor_ring

#eval do
  IO.println "Processed rank-3 minor evaluations 150/167"
  (← IO.getStdout).flush

def original_minor_3_185 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 4, 6])

theorem original_minor_3_185_value (w : Fin 8 → ℂ) :
    original_minor_3_185 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 5) 2))) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (128 : ℂ) (w 0)) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 1)) (cpow (w 5) 2)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 5) 2)) (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 4)) (cpow (w 5) 2))) (cadd (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (cpow (w 5) 3)) (cmul (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 4)) (w 5)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (96 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (96 : ℂ) Complex.I) (cpow (w 5) 2)) (cpow (w 7) 2))))))) := by
  unfold original_minor_3_185
  simp only [det_fin_four]
  minor_ring

def original_minor_3_186 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 5, 6])

theorem original_minor_3_186_value (w : Fin 8 → ℂ) :
    original_minor_3_186 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 1)) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (w 3)) (w 6)))) (cadd (cmul (cmul (-32 : ℂ) (cpow (w 2) 2)) (cpow (w 5) 2)) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2)))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7)))))) := by
  unfold original_minor_3_186
  simp only [det_fin_four]
  minor_ring

def original_minor_3_187 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 5, 7])

theorem original_minor_3_187_value (w : Fin 8 → ℂ) :
    original_minor_3_187 w =
    (cadd (cmul (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 5) 2)) (w 6)))) := by
  unfold original_minor_3_187
  simp only [det_fin_four]
  minor_ring

def original_minor_3_188 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 5, 8])

theorem original_minor_3_188_value (w : Fin 8 → ℂ) :
    original_minor_3_188 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 5)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 3)) (w 6)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (-8 : ℂ) (cpow (w 2) 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 2) 2)) (w 5)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (w 2)) (cpow (w 4) 2)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 2)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (cpow (w 6) 2)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) (w 4)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 4)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 5)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (96 : ℂ) (w 5)) (w 6)) (cpow (w 7) 2))))))) := by
  unfold original_minor_3_188
  simp only [det_fin_four]
  minor_ring

def original_minor_3_189 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 5, 9])

theorem original_minor_3_189_value (w : Fin 8 → ℂ) :
    original_minor_3_189 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) (w 0)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (cpow (w 5) 2)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (24 : ℂ) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-88 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (56 : ℂ) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (cpow (w 5) 2)) (w 6)) (w 7)))))) := by
  unfold original_minor_3_189
  simp only [det_fin_four]
  minor_ring

def original_minor_3_190 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 5, 11])

theorem original_minor_3_190_value (w : Fin 8 → ℂ) :
    original_minor_3_190 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 4)) (w 5)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (w 6)) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (-64 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (16 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (-112 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-96 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7)))))) := by
  unfold original_minor_3_190
  simp only [det_fin_four]
  minor_ring

def original_minor_3_191 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 6, 7])

theorem original_minor_3_191_value (w : Fin 8 → ℂ) :
    original_minor_3_191 w =
    (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (cpow (w 5) 3)))) := by
  unfold original_minor_3_191
  simp only [det_fin_four]
  minor_ring

def original_minor_3_192 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 2, 6, 9])

theorem original_minor_3_192_value (w : Fin 8 → ℂ) :
    original_minor_3_192 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 2)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 3)))) (cadd (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 4)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 3)) (cmul (cmul (cmul (-32 : ℂ) (cpow (w 2) 2)) (w 5)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 3)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 2)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (-176 : ℂ) (w 2)) (cpow (w 5) 2)) (w 7)))) (cadd (cmul (cmul (cmul (16 : ℂ) (cpow (w 4) 2)) (w 5)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-112 : ℂ) Complex.I) (w 4)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (-96 : ℂ) (cpow (w 5) 3)) (w 7)))))) := by
  unfold original_minor_3_192
  simp only [det_fin_four]
  minor_ring

def original_minor_3_193 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 3, 4, 5])

theorem original_minor_3_193_value (w : Fin 8 → ℂ) :
    original_minor_3_193 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (8 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 3)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 6) 3)) (cadd (cmul (cmul (cmul (-64 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (48 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 6) 3)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 6) 2)))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 3)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2))))) (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7)))) (cadd (cmul (cmul (-56 : ℂ) (cpow (w 6) 3)) (w 7)) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (-40 : ℂ) (w 6)) (cpow (w 7) 3))))))) := by
  unfold original_minor_3_193
  simp only [det_fin_four]
  minor_ring

def original_minor_3_194 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 3, 5, 6])

theorem original_minor_3_194_value (w : Fin 8 → ℂ) :
    original_minor_3_194 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (w 6)) (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 1)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 2)) (cpow (w 5) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 3)) (w 4)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (-32 : ℂ) (w 0)) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (-16 : ℂ) (w 0)) (w 4)) (cpow (w 6) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 3))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 5)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 0)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 4)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 1) 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 3)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (cpow (w 6) 2)))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 3)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 3)) (w 5)) (w 6))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 4)) (cpow (w 5) 2)) (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 4)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 4)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 3)) (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 5)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 1)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (cpow (w 3) 2)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 3)) (cpow (w 5) 2)))) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 3)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (cpow (w 5) 2)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (cmul (16 : ℂ) (w 2)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 3)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-48 : ℂ) (w 3)) (w 5)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-96 : ℂ) Complex.I) (w 4)) (cpow (w 5) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-56 : ℂ) Complex.I) (w 4)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (-112 : ℂ) (w 4)) (w 6)) (cpow (w 7) 2)))) (cadd (cmul (cmul (-96 : ℂ) (cpow (w 5) 3)) (w 7)) (cadd (cmul (cmul (cmul (-56 : ℂ) (w 5)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (112 : ℂ) Complex.I) (w 5)) (w 6)) (cpow (w 7) 2)))))))) := by
  unfold original_minor_3_194
  simp only [det_fin_four]
  minor_ring

#eval do
  IO.println "Processed rank-3 minor evaluations 160/167"
  (← IO.getStdout).flush

def original_minor_3_195 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 3, 5, 7])

theorem original_minor_3_195_value (w : Fin 8 → ℂ) :
    original_minor_3_195 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (w 6))) (cadd (cmul (cmul (cmul (-24 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (-24 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-16 : ℂ) (cpow (w 4) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (72 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (56 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7)))))) := by
  unfold original_minor_3_195
  simp only [det_fin_four]
  minor_ring

def original_minor_3_196 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![0, 4, 5, 6])

theorem original_minor_3_196_value (w : Fin 8 → ℂ) :
    original_minor_3_196 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 6)) (cmul (cmul (cmul (32 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 5) 2)))) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 0) 2)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (32 : ℂ) (cpow (w 0) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 1)) (w 3)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 5) 2)) (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2)))) (cadd (cmul (cmul (cmul (cmul (48 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 3)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-64 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6)) (cadd (cmul (cmul (cmul (-128 : ℂ) (w 0)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (cpow (w 6) 3)))) (cadd (cmul (cmul (cmul (-40 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (144 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 1) 2)) (cpow (w 6) 2))))) (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 2)) (w 4)) (w 6)))) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 3)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 1)) (w 3)) (w 6)) (w 7))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (w 6)) (cadd (cmul (cmul (cmul (16 : ℂ) (w 1)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (cpow (w 6) 3)))) (cadd (cmul (cmul (cmul (40 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 3)) (w 4)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) (w 2)) (w 4)) (cpow (w 5) 2)))))) (cadd (cadd (cadd (cmul (cmul (cmul (-8 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (cpow (w 5) 3)))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-48 : ℂ) (w 3)) (cpow (w 6) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-48 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (-96 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (-96 : ℂ) Complex.I) (cpow (w 5) 2)) (cpow (w 7) 2)))) (cadd (cmul (cmul (-56 : ℂ) (cpow (w 6) 3)) (w 7)) (cadd (cmul (cmul (cmul (56 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (-112 : ℂ) (w 6)) (cpow (w 7) 3)))))))) := by
  unfold original_minor_3_196
  simp only [det_fin_four]
  minor_ring

def original_minor_3_198 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 1, 5, 6] ![2, 3, 5, 6])

theorem original_minor_3_198_value (w : Fin 8 → ℂ) :
    original_minor_3_198 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 4) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (w 6))))) (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 3)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 5) 2))) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2)) (cadd (cmul (cmul (cmul (cmul (32 : ℂ) (w 2)) (w 4)) (w 6)) (w 7)) (cmul (cmul (32 : ℂ) (w 2)) (cpow (w 5) 3)))))) (cadd (cadd (cadd (cmul (cmul (cmul (16 : ℂ) (w 2)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 3)) (cpow (w 4) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 3)) (w 4)) (w 5)) (w 6)) (cmul (cmul (-16 : ℂ) (cpow (w 4) 2)) (cpow (w 5) 2))))) (cadd (cadd (cmul (cmul (-8 : ℂ) (cpow (w 4) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 4)) (cpow (w 5) 3)) (cadd (cmul (cmul (-8 : ℂ) (cpow (w 5) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (cpow (w 5) 2)) (w 6)) (w 7))))))) := by
  unfold original_minor_3_198
  simp only [det_fin_four]
  minor_ring

def original_minor_3_199 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![0, 4, 5, 6] ![0, 1, 2, 5])

theorem original_minor_3_199_value (w : Fin 8 → ℂ) :
    original_minor_3_199 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (48 : ℂ) (w 6)) (cpow (w 7) 3)))))) := by
  unfold original_minor_3_199
  simp only [det_fin_four]
  minor_ring

def original_minor_3_204 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![1, 4, 5, 6] ![0, 1, 2, 6])

theorem original_minor_3_204_value (w : Fin 8 → ℂ) :
    original_minor_3_204 w =
    (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (-16 : ℂ) (w 1)) (w 4)) (w 5)) (w 7))) (cadd (cmul (cmul (16 : ℂ) (cpow (w 2) 2)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 5) 2))))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (-32 : ℂ) (w 2)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (16 : ℂ) (w 3)) (w 4)) (w 5)) (w 7)))) (cadd (cmul (cmul (-16 : ℂ) (cpow (w 4) 2)) (cpow (w 5) 2)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 4)) (w 5)) (cpow (w 7) 2)))))) := by
  unfold original_minor_3_204
  simp only [det_fin_four]
  minor_ring

def original_minor_3_205 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![1, 4, 5, 6] ![0, 2, 3, 5])

theorem original_minor_3_205_value (w : Fin 8 → ℂ) :
    original_minor_3_205 w =
    (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 1)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 1)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 3)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 4)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-32 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (cpow (w 6) 3))))) (cadd (cadd (cadd (cmul (cmul (cmul (-40 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-8 : ℂ) Complex.I) (cpow (w 1) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 3)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 4)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (cpow (w 6) 3))))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (24 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-16 : ℂ) Complex.I) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (24 : ℂ) (w 2)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 2)) (w 5)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (72 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (8 : ℂ) (cpow (w 3) 2)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 3)) (w 4)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (64 : ℂ) (w 3)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (-56 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (8 : ℂ) Complex.I) (cpow (w 4) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (-8 : ℂ) (w 4)) (w 5)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (56 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (96 : ℂ) (cpow (w 5) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (56 : ℂ) (cpow (w 6) 3)) (w 7)) (cadd (cmul (cmul (cmul (-152 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (-80 : ℂ) (w 6)) (cpow (w 7) 3)))))))) := by
  unfold original_minor_3_205
  simp only [det_fin_four]
  minor_ring

def original_minor_3_208 (w : Fin 8 → ℂ) : ℂ :=
  Matrix.det ((normalMatrix w).submatrix ![1, 4, 5, 6] ![0, 2, 5, 9])

theorem original_minor_3_208_value (w : Fin 8 → ℂ) :
    original_minor_3_208 w =
    (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 0)) (w 3)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (cmul (-8 : ℂ) (w 0)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (8 : ℂ) (w 0)) (cpow (w 6) 2)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (-16 : ℂ) Complex.I) (w 0)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 1) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (16 : ℂ) (w 1)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (cmul (-8 : ℂ) (w 1)) (w 4)) (w 5)) (w 6)))))) (cadd (cadd (cadd (cmul (cmul (cmul (8 : ℂ) (w 1)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (-40 : ℂ) Complex.I) (w 1)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (-8 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-24 : ℂ) (w 2)) (w 5)) (w 6)) (w 7)) (cmul (cmul (cmul (-8 : ℂ) (cpow (w 3) 2)) (w 6)) (w 7))))) (cadd (cadd (cmul (cmul (cmul (cmul (8 : ℂ) (w 3)) (w 4)) (w 5)) (w 6)) (cadd (cmul (cmul (cmul (-8 : ℂ) (w 3)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (cmul (40 : ℂ) Complex.I) (w 3)) (w 6)) (cpow (w 7) 2)))) (cadd (cmul (cmul (cmul (cmul (cmul (-24 : ℂ) Complex.I) (w 4)) (w 5)) (w 6)) (w 7)) (cadd (cmul (cmul (cmul (24 : ℂ) Complex.I) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (48 : ℂ) (w 6)) (cpow (w 7) 3))))))) := by
  unfold original_minor_3_208
  simp only [det_fin_four]
  minor_ring

#eval do
  IO.println "Processed rank-3 minor evaluations 167/167"
  (← IO.getStdout).flush

def certificate_3_68_target (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cmul (1 : ℂ) (cpow (w 6) 4)) (cmul (cmul (cmul (-6 : ℂ) Complex.I) (cpow (w 6) 3)) (w 7))) (cadd (cmul (cmul (-12 : ℂ) (cpow (w 6) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (8 : ℂ) Complex.I) (w 6)) (cpow (w 7) 3))))

def certificate_3_68_chunk_0 (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cadd (cmul (cmul (4 : ℂ) Complex.I) (original_minor_3_0 w)) (cmul (cmul (-4 : ℂ) Complex.I) (original_minor_3_3 w))) (cadd (cmul (cmul (16 : ℂ) Complex.I) (original_minor_3_6 w)) (cmul (4 : ℂ) (original_minor_3_7 w)))) (cadd (cadd (cmul (cmul (-8 : ℂ) Complex.I) (original_minor_3_9 w)) (cmul (-2 : ℂ) (original_minor_3_11 w))) (cadd (cmul (2 : ℂ) (original_minor_3_12 w)) (cmul (cmul (-5 : ℂ) Complex.I) (original_minor_3_15 w))))) (cadd (cadd (cadd (cmul (cmul (-8 : ℂ) Complex.I) (original_minor_3_17 w)) (cmul (8 : ℂ) (original_minor_3_18 w))) (cadd (cmul (8 : ℂ) (original_minor_3_19 w)) (cmul (cmul (-8 : ℂ) Complex.I) (original_minor_3_22 w)))) (cadd (cadd (cmul (4 : ℂ) (original_minor_3_23 w)) (cmul (cmul (4 : ℂ) Complex.I) (original_minor_3_25 w))) (cadd (cmul (cmul (4 : ℂ) Complex.I) (original_minor_3_30 w)) (cmul (cmul (12 : ℂ) Complex.I) (original_minor_3_33 w))))))

def certificate_3_68_chunk_0_polynomial (w : Fin 8 → ℂ) : ℂ :=
    (cadd (cadd (cadd (cadd (cadd (cadd (cadd (cmul (-32 : ℂ) (cpow (w 0) 4)) (cmul (cmul (-32 : ℂ) (cpow (w 0) 3)) (w 1))) (cadd (cmul (cmul (96 : ℂ) (cpow (w 0) 3)) (w 3)) (cmul (cmul (cmul (-384 : ℂ) Complex.I) (cpow (w 0) 3)) (w 7)))) (cadd (cadd (cmul (cmul (192 : ℂ) (cpow (w 0) 2)) (cpow (w 1) 2)) (cmul (cmul (cmul (-448 : ℂ) (cpow (w 0) 2)) (w 1)) (w 6))) (cadd (cmul (cmul (cmul (cmul (608 : ℂ) Complex.I) (cpow (w 0) 2)) (w 1)) (w 7)) (cmul (cmul (160 : ℂ) (cpow (w 0) 2)) (cpow (w 2) 2))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (384 : ℂ) Complex.I) (cpow (w 0) 2)) (w 2)) (w 4)) (cmul (cmul (cmul (352 : ℂ) (cpow (w 0) 2)) (w 2)) (w 5))) (cadd (cmul (cmul (-192 : ℂ) (cpow (w 0) 2)) (cpow (w 3) 2)) (cmul (cmul (cmul (160 : ℂ) (cpow (w 0) 2)) (w 3)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (544 : ℂ) Complex.I) (cpow (w 0) 2)) (w 3)) (w 7)) (cmul (cmul (-224 : ℂ) (cpow (w 0) 2)) (cpow (w 4) 2))) (cadd (cmul (cmul (cmul (cmul (736 : ℂ) Complex.I) (cpow (w 0) 2)) (w 4)) (w 5)) (cmul (cmul (768 : ℂ) (cpow (w 0) 2)) (cpow (w 5) 2)))))) (cadd (cadd (cadd (cadd (cmul (cmul (312 : ℂ) (cpow (w 0) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-1248 : ℂ) Complex.I) (cpow (w 0) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (480 : ℂ) (cpow (w 0) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (128 : ℂ) (w 0)) (cpow (w 1) 2)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (896 : ℂ) Complex.I) (w 0)) (cpow (w 1) 2)) (w 7)) (cmul (cmul (cmul (-320 : ℂ) (w 0)) (w 1)) (cpow (w 2) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (-384 : ℂ) Complex.I) (w 0)) (w 1)) (w 2)) (w 4)) (cmul (cmul (cmul (cmul (-256 : ℂ) (w 0)) (w 1)) (w 2)) (w 5))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (192 : ℂ) (w 0)) (w 1)) (w 3)) (w 6)) (cmul (cmul (cmul (cmul (cmul (-384 : ℂ) Complex.I) (w 0)) (w 1)) (w 3)) (w 7))) (cadd (cmul (cmul (cmul (64 : ℂ) (w 0)) (w 1)) (cpow (w 4) 2)) (cmul (cmul (cmul (cmul (cmul (128 : ℂ) Complex.I) (w 0)) (w 1)) (w 4)) (w 5)))) (cadd (cadd (cmul (cmul (cmul (192 : ℂ) (w 0)) (w 1)) (cpow (w 5) 2)) (cmul (cmul (cmul (-160 : ℂ) (w 0)) (w 1)) (cpow (w 6) 2))) (cadd (cmul (cmul (cmul (cmul (cmul (-2048 : ℂ) Complex.I) (w 0)) (w 1)) (w 6)) (w 7)) (cmul (cmul (cmul (-3872 : ℂ) (w 0)) (w 1)) (cpow (w 7) 2))))))) (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (-64 : ℂ) (w 0)) (cpow (w 2) 2)) (w 3)) (cmul (cmul (cmul (416 : ℂ) (w 0)) (cpow (w 2) 2)) (w 6))) (cadd (cmul (cmul (cmul (cmul (128 : ℂ) Complex.I) (w 0)) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-384 : ℂ) Complex.I) (w 0)) (w 2)) (w 3)) (w 4)))) (cadd (cadd (cmul (cmul (cmul (cmul (-512 : ℂ) (w 0)) (w 2)) (w 3)) (w 5)) (cmul (cmul (cmul (cmul (cmul (480 : ℂ) Complex.I) (w 0)) (w 2)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-1344 : ℂ) (w 0)) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (-128 : ℂ) (w 0)) (w 2)) (w 5)) (w 6))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (2368 : ℂ) Complex.I) (w 0)) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (-320 : ℂ) (w 0)) (cpow (w 3) 2)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-512 : ℂ) Complex.I) (w 0)) (cpow (w 3) 2)) (w 7)) (cmul (cmul (cmul (320 : ℂ) (w 0)) (w 3)) (cpow (w 4) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-896 : ℂ) Complex.I) (w 0)) (w 3)) (w 4)) (w 5)) (cmul (cmul (cmul (-576 : ℂ) (w 0)) (w 3)) (cpow (w 5) 2))) (cadd (cmul (cmul (cmul (-256 : ℂ) (w 0)) (w 3)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (1984 : ℂ) Complex.I) (w 0)) (w 3)) (w 6)) (w 7)))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (352 : ℂ) (w 0)) (w 3)) (cpow (w 7) 2)) (cmul (cmul (cmul (-128 : ℂ) (w 0)) (cpow (w 4) 2)) (w 6))) (cadd (cmul (cmul (cmul (cmul (-1088 : ℂ) Complex.I) (w 0)) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-64 : ℂ) Complex.I) (w 0)) (w 4)) (w 5)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (-4544 : ℂ) (w 0)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (128 : ℂ) (w 0)) (cpow (w 5) 2)) (w 6))) (cadd (cmul (cmul (cmul (cmul (4352 : ℂ) Complex.I) (w 0)) (cpow (w 5) 2)) (w 7)) (cmul (cmul (64 : ℂ) (w 0)) (cpow (w 6) 3))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (1488 : ℂ) Complex.I) (w 0)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (6720 : ℂ) (w 0)) (w 6)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-3520 : ℂ) Complex.I) (w 0)) (cpow (w 7) 3)) (cmul (cmul (128 : ℂ) (cpow (w 1) 2)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (-128 : ℂ) Complex.I) (cpow (w 1) 2)) (w 6)) (w 7)) (cmul (cmul (-1472 : ℂ) (cpow (w 1) 2)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (-128 : ℂ) (w 1)) (cpow (w 2) 2)) (w 6)) (cadd (cmul (cmul (cmul (cmul (-704 : ℂ) Complex.I) (w 1)) (cpow (w 2) 2)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-160 : ℂ) Complex.I) (w 1)) (w 2)) (w 4)) (w 6))))))))) (cadd (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (832 : ℂ) (w 1)) (w 2)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (-544 : ℂ) (w 1)) (w 2)) (w 5)) (w 6))) (cadd (cmul (cmul (cmul (cmul (cmul (320 : ℂ) Complex.I) (w 1)) (w 2)) (w 5)) (w 7)) (cmul (cmul (cmul (-128 : ℂ) (w 1)) (w 3)) (cpow (w 6) 2)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (1088 : ℂ) Complex.I) (w 1)) (w 3)) (w 6)) (w 7)) (cmul (cmul (cmul (1664 : ℂ) (w 1)) (w 3)) (cpow (w 7) 2))) (cadd (cmul (cmul (cmul (32 : ℂ) (w 1)) (cpow (w 4) 2)) (w 6)) (cmul (cmul (cmul (cmul (128 : ℂ) Complex.I) (w 1)) (cpow (w 4) 2)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-384 : ℂ) Complex.I) (w 1)) (w 4)) (w 5)) (w 6)) (cmul (cmul (cmul (cmul (-1152 : ℂ) (w 1)) (w 4)) (w 5)) (w 7))) (cadd (cmul (cmul (cmul (-352 : ℂ) (w 1)) (cpow (w 5) 2)) (w 6)) (cmul (cmul (cmul (cmul (1280 : ℂ) Complex.I) (w 1)) (cpow (w 5) 2)) (w 7)))) (cadd (cadd (cmul (cmul (-128 : ℂ) (w 1)) (cpow (w 6) 3)) (cmul (cmul (cmul (cmul (288 : ℂ) Complex.I) (w 1)) (cpow (w 6) 2)) (w 7))) (cadd (cmul (cmul (cmul (3648 : ℂ) (w 1)) (w 6)) (cpow (w 7) 2)) (cmul (cmul (cmul (-6304 : ℂ) Complex.I) (w 1)) (cpow (w 7) 3)))))) (cadd (cadd (cadd (cadd (cmul (128 : ℂ) (cpow (w 2) 4)) (cmul (cmul (cmul (256 : ℂ) Complex.I) (cpow (w 2) 3)) (w 4))) (cadd (cmul (cmul (192 : ℂ) (cpow (w 2) 3)) (w 5)) (cmul (cmul (cmul (-224 : ℂ) (cpow (w 2) 2)) (w 3)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (256 : ℂ) Complex.I) (cpow (w 2) 2)) (w 3)) (w 7)) (cmul (cmul (cmul (cmul (-448 : ℂ) Complex.I) (cpow (w 2) 2)) (w 4)) (w 5))) (cadd (cmul (cmul (160 : ℂ) (cpow (w 2) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (608 : ℂ) Complex.I) (cpow (w 2) 2)) (w 6)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (416 : ℂ) (cpow (w 2) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (cmul (-544 : ℂ) Complex.I) (w 2)) (w 3)) (w 4)) (w 6))) (cadd (cmul (cmul (cmul (cmul (64 : ℂ) (w 2)) (w 3)) (w 4)) (w 7)) (cmul (cmul (cmul (cmul (-160 : ℂ) (w 2)) (w 3)) (w 5)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (cmul (-1216 : ℂ) Complex.I) (w 2)) (w 3)) (w 5)) (w 7)) (cmul (cmul (cmul (256 : ℂ) Complex.I) (w 2)) (cpow (w 4) 3))) (cadd (cmul (cmul (cmul (1472 : ℂ) (w 2)) (cpow (w 4) 2)) (w 5)) (cmul (cmul (cmul (cmul (-1280 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 5) 2))))))) (cadd (cadd (cadd (cadd (cadd (cmul (cmul (cmul (cmul (32 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-1312 : ℂ) (w 2)) (w 4)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-704 : ℂ) Complex.I) (w 2)) (w 4)) (cpow (w 7) 2)) (cmul (cmul (-64 : ℂ) (w 2)) (cpow (w 5) 3)))) (cadd (cadd (cmul (cmul (cmul (-32 : ℂ) (w 2)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (cmul (-256 : ℂ) Complex.I) (w 2)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (-3808 : ℂ) (w 2)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (-960 : ℂ) Complex.I) (cpow (w 3) 2)) (w 6)) (w 7))))) (cadd (cadd (cadd (cmul (cmul (-192 : ℂ) (cpow (w 3) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (320 : ℂ) (w 3)) (cpow (w 4) 2)) (w 6))) (cadd (cmul (cmul (cmul (cmul (320 : ℂ) Complex.I) (w 3)) (cpow (w 4) 2)) (w 7)) (cmul (cmul (cmul (cmul (cmul (-320 : ℂ) Complex.I) (w 3)) (w 4)) (w 5)) (w 6)))) (cadd (cadd (cmul (cmul (cmul (cmul (2048 : ℂ) (w 3)) (w 4)) (w 5)) (w 7)) (cmul (cmul (cmul (cmul (-1728 : ℂ) Complex.I) (w 3)) (cpow (w 5) 2)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-768 : ℂ) Complex.I) (w 3)) (cpow (w 6) 2)) (w 7)) (cmul (cmul (cmul (-4512 : ℂ) (w 3)) (w 6)) (cpow (w 7) 2)))))) (cadd (cadd (cadd (cadd (cmul (cmul (cmul (3360 : ℂ) Complex.I) (w 3)) (cpow (w 7) 3)) (cmul (-128 : ℂ) (cpow (w 4) 4))) (cadd (cmul (cmul (cmul (832 : ℂ) Complex.I) (cpow (w 4) 3)) (w 5)) (cmul (cmul (1280 : ℂ) (cpow (w 4) 2)) (cpow (w 5) 2)))) (cadd (cadd (cmul (cmul (96 : ℂ) (cpow (w 4) 2)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-768 : ℂ) Complex.I) (cpow (w 4) 2)) (w 6)) (w 7))) (cadd (cmul (cmul (864 : ℂ) (cpow (w 4) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (-576 : ℂ) Complex.I) (w 4)) (cpow (w 5) 3))))) (cadd (cadd (cadd (cmul (cmul (cmul (cmul (-192 : ℂ) Complex.I) (w 4)) (w 5)) (cpow (w 6) 2)) (cmul (cmul (cmul (cmul (-576 : ℂ) (w 4)) (w 5)) (w 6)) (w 7))) (cadd (cmul (cmul (cmul (cmul (-6240 : ℂ) Complex.I) (w 4)) (w 5)) (cpow (w 7) 2)) (cmul (cmul (cmul (cmul (384 : ℂ) Complex.I) (cpow (w 5) 2)) (w 6)) (w 7)))) (cadd (cadd (cmul (cmul (-6144 : ℂ) (cpow (w 5) 2)) (cpow (w 7) 2)) (cmul (cmul (cmul (192 : ℂ) Complex.I) (cpow (w 6) 3)) (w 7))) (cadd (cmul (cmul (-1656 : ℂ) (cpow (w 6) 2)) (cpow (w 7) 2)) (cadd (cmul (cmul (cmul (8928 : ℂ) Complex.I) (w 6)) (cpow (w 7) 3)) (cmul (7104 : ℂ) (cpow (w 7) 4))))))))))

theorem certificate_3_68_chunk_0_identity (w : Fin 8 → ℂ) :
    certificate_3_68_chunk_0 w = certificate_3_68_chunk_0_polynomial w := by
  unfold certificate_3_68_chunk_0 certificate_3_68_chunk_0_polynomial
  simp only [original_minor_3_0_value, original_minor_3_3_value, original_minor_3_6_value, original_minor_3_7_value, original_minor_3_9_value, original_minor_3_11_value, original_minor_3_12_value, original_minor_3_15_value, original_minor_3_17_value, original_minor_3_18_value, original_minor_3_19_value, original_minor_3_22_value, original_minor_3_23_value, original_minor_3_25_value, original_minor_3_30_value, original_minor_3_33_value]
  gaussian_ring

#eval do
  IO.println "Processed certificate_3_68_chunk_0"
  (← IO.getStdout).flush


end ValyuResearch.ElasticityMinorCertificates
