import Residual32ContextsProof.Catalog
import Catalog
open scoped BigOperators
open ErdosSzekeres
namespace OmissionResidual32Transfer
set_option maxRecDepth 100000
set_option maxHeartbeats 100000000

theorem original_chunk_0 : ∀ r : Fin 128,
    OmissionResidual32Contexts.support ⟨0 + r.val, by omega⟩ = OmissionResidual.support ⟨0 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨0 + r.val, by omega⟩ = OmissionResidual.demand ⟨0 + r.val, by omega⟩ := by
  decide +kernel

theorem original_chunk_128 : ∀ r : Fin 128,
    OmissionResidual32Contexts.support ⟨128 + r.val, by omega⟩ = OmissionResidual.support ⟨128 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨128 + r.val, by omega⟩ = OmissionResidual.demand ⟨128 + r.val, by omega⟩ := by
  decide +kernel

theorem original_chunk_256 : ∀ r : Fin 128,
    OmissionResidual32Contexts.support ⟨256 + r.val, by omega⟩ = OmissionResidual.support ⟨256 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨256 + r.val, by omega⟩ = OmissionResidual.demand ⟨256 + r.val, by omega⟩ := by
  decide +kernel

theorem original_chunk_384 : ∀ r : Fin 128,
    OmissionResidual32Contexts.support ⟨384 + r.val, by omega⟩ = OmissionResidual.support ⟨384 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨384 + r.val, by omega⟩ = OmissionResidual.demand ⟨384 + r.val, by omega⟩ := by
  decide +kernel

theorem original_chunk_512 : ∀ r : Fin 128,
    OmissionResidual32Contexts.support ⟨512 + r.val, by omega⟩ = OmissionResidual.support ⟨512 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨512 + r.val, by omega⟩ = OmissionResidual.demand ⟨512 + r.val, by omega⟩ := by
  decide +kernel

theorem original_chunk_640 : ∀ r : Fin 128,
    OmissionResidual32Contexts.support ⟨640 + r.val, by omega⟩ = OmissionResidual.support ⟨640 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨640 + r.val, by omega⟩ = OmissionResidual.demand ⟨640 + r.val, by omega⟩ := by
  decide +kernel

theorem original_chunk_768 : ∀ r : Fin 128,
    OmissionResidual32Contexts.support ⟨768 + r.val, by omega⟩ = OmissionResidual.support ⟨768 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨768 + r.val, by omega⟩ = OmissionResidual.demand ⟨768 + r.val, by omega⟩ := by
  decide +kernel

theorem original_chunk_896 : ∀ r : Fin 128,
    OmissionResidual32Contexts.support ⟨896 + r.val, by omega⟩ = OmissionResidual.support ⟨896 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨896 + r.val, by omega⟩ = OmissionResidual.demand ⟨896 + r.val, by omega⟩ := by
  decide +kernel

theorem original_chunk_1024 : ∀ r : Fin 128,
    OmissionResidual32Contexts.support ⟨1024 + r.val, by omega⟩ = OmissionResidual.support ⟨1024 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨1024 + r.val, by omega⟩ = OmissionResidual.demand ⟨1024 + r.val, by omega⟩ := by
  decide +kernel

theorem original_chunk_1152 : ∀ r : Fin 35,
    OmissionResidual32Contexts.support ⟨1152 + r.val, by omega⟩ = OmissionResidual.support ⟨1152 + r.val, by omega⟩ ∧
    OmissionResidual32Contexts.demand ⟨1152 + r.val, by omega⟩ = OmissionResidual.demand ⟨1152 + r.val, by omega⟩ := by
  decide +kernel

theorem original_matches (r : Fin 1187) :
    OmissionResidual32Contexts.support ⟨0 + r.val, by omega⟩ = OmissionResidual.support r ∧
    OmissionResidual32Contexts.demand ⟨0 + r.val, by omega⟩ = OmissionResidual.demand r := by
  by_cases h0 : r.val < 128
  · let k : Fin 128 := ⟨r.val - 0, by omega⟩
    have hk : 0 + k.val = r.val := by dsimp [k]; omega
    have he : (0 + k.val) = 0 + r.val := by omega
    have hi : (⟨0 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_0 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  by_cases h128 : r.val < 256
  · let k : Fin 128 := ⟨r.val - 128, by omega⟩
    have hk : 128 + k.val = r.val := by dsimp [k]; omega
    have he : (128 + k.val) = 0 + r.val := by omega
    have hi : (⟨128 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_128 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  by_cases h256 : r.val < 384
  · let k : Fin 128 := ⟨r.val - 256, by omega⟩
    have hk : 256 + k.val = r.val := by dsimp [k]; omega
    have he : (256 + k.val) = 0 + r.val := by omega
    have hi : (⟨256 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_256 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  by_cases h384 : r.val < 512
  · let k : Fin 128 := ⟨r.val - 384, by omega⟩
    have hk : 384 + k.val = r.val := by dsimp [k]; omega
    have he : (384 + k.val) = 0 + r.val := by omega
    have hi : (⟨384 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_384 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  by_cases h512 : r.val < 640
  · let k : Fin 128 := ⟨r.val - 512, by omega⟩
    have hk : 512 + k.val = r.val := by dsimp [k]; omega
    have he : (512 + k.val) = 0 + r.val := by omega
    have hi : (⟨512 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_512 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  by_cases h640 : r.val < 768
  · let k : Fin 128 := ⟨r.val - 640, by omega⟩
    have hk : 640 + k.val = r.val := by dsimp [k]; omega
    have he : (640 + k.val) = 0 + r.val := by omega
    have hi : (⟨640 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_640 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  by_cases h768 : r.val < 896
  · let k : Fin 128 := ⟨r.val - 768, by omega⟩
    have hk : 768 + k.val = r.val := by dsimp [k]; omega
    have he : (768 + k.val) = 0 + r.val := by omega
    have hi : (⟨768 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_768 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  by_cases h896 : r.val < 1024
  · let k : Fin 128 := ⟨r.val - 896, by omega⟩
    have hk : 896 + k.val = r.val := by dsimp [k]; omega
    have he : (896 + k.val) = 0 + r.val := by omega
    have hi : (⟨896 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_896 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  by_cases h1024 : r.val < 1152
  · let k : Fin 128 := ⟨r.val - 1024, by omega⟩
    have hk : 1024 + k.val = r.val := by dsimp [k]; omega
    have he : (1024 + k.val) = 0 + r.val := by omega
    have hi : (⟨1024 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_1024 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  by_cases h1152 : r.val < 1187
  · let k : Fin 35 := ⟨r.val - 1152, by omega⟩
    have hk : 1152 + k.val = r.val := by dsimp [k]; omega
    have he : (1152 + k.val) = 0 + r.val := by omega
    have hi : (⟨1152 + k.val, by omega⟩ : Fin 1187) = r := Fin.ext hk
    have hchunk := original_chunk_1152 k
    rw [hi] at hchunk
    simpa only [he] using hchunk
  omega
#print axioms original_matches
end OmissionResidual32Transfer
