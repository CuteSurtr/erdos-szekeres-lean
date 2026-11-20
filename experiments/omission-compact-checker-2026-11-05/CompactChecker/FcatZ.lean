import CompactChecker.Fcat62
namespace CompactChecker
-- FV304 (20 November 2026): fcatZ = fcat62 (the 3,131 rows of balanced-v2-source.json, sha256 acaf6323...) with the
-- Z-row added as row 3131 (demand 15, support OmissionZRow.zIndices; source fcatz-source.json sha256 94cd9281...).
-- The trie is the one make_fcat.py builds for the 3,132 rows; every subtree off the path to row 3131 is fcat62's own
-- constant, so fcatZ_wf follows from fcat62_wf plus a kernel check of the new row.
noncomputable def fcatZ_r3131 : FCat := FCat.row [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 29, 31, 32, 33, 34, 35, 36, 40, 42, 43, 44, 46, 47, 48, 49, 55, 57, 58, 60, 61, 62, 63, 72, 73, 75, 77, 78, 79, 80, 90, 93, 94, 96, 97, 108, 112, 114, 115, 116, 130, 133, 134, 151, 153, 170, 187] 15 (codeL 4194304 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 25, 26, 29, 31, 32, 33, 34, 35, 36, 40, 42, 43, 44, 46, 47, 48, 49, 55, 57, 58, 60, 61, 62, 63, 72, 73, 75, 77, 78, 79, 80, 90, 93, 94, 96, 97, 108, 112, 114, 115, 116, 130, 133, 134, 151, 153, 170, 187])
noncomputable def fcatZ_n11011100001 : FCat := FCat.node fcat62_r1083 fcatZ_r3131
noncomputable def fcatZ_n1101110000 : FCat := FCat.node fcat62_n11011100000 fcatZ_n11011100001
noncomputable def fcatZ_n110111000 : FCat := FCat.node fcatZ_n1101110000 fcat62_n1101110001
noncomputable def fcatZ_n11011100 : FCat := FCat.node fcatZ_n110111000 fcat62_n110111001
noncomputable def fcatZ_n1101110 : FCat := FCat.node fcatZ_n11011100 fcat62_n11011101
noncomputable def fcatZ_n110111 : FCat := FCat.node fcatZ_n1101110 fcat62_n1101111
noncomputable def fcatZ_n11011 : FCat := FCat.node fcat62_n110110 fcatZ_n110111
noncomputable def fcatZ_n1101 : FCat := FCat.node fcat62_n11010 fcatZ_n11011
noncomputable def fcatZ_n110 : FCat := FCat.node fcat62_n1100 fcatZ_n1101
noncomputable def fcatZ_n11 : FCat := FCat.node fcatZ_n110 fcat62_n111
noncomputable def fcatZ_n1 : FCat := FCat.node fcat62_n10 fcatZ_n11
noncomputable def fcatZ : FCat := FCat.node fcat62_n0 fcatZ_n1

theorem FCat.wf_node {n b : ℕ} {l r : FCat} :
    (FCat.node l r).wf n b = true ↔ l.wf n b = true ∧ r.wf n b = true := by
  simp [FCat.wf]

theorem fcatZ_r3131_wf : fcatZ_r3131.wf 252 4194304 = true := by decide +kernel

theorem fcatZ_wf : fcatZ.wf 252 4194304 = true := by
  have a0 := FCat.wf_node.mp (show (FCat.node fcat62_n0 fcat62_n1).wf 252 4194304 = true from fcat62_wf)
  have a1 := FCat.wf_node.mp (show (FCat.node fcat62_n10 fcat62_n11).wf 252 4194304 = true from a0.2)
  have a2 := FCat.wf_node.mp (show (FCat.node fcat62_n110 fcat62_n111).wf 252 4194304 = true from a1.2)
  have a3 := FCat.wf_node.mp (show (FCat.node fcat62_n1100 fcat62_n1101).wf 252 4194304 = true from a2.1)
  have a4 := FCat.wf_node.mp (show (FCat.node fcat62_n11010 fcat62_n11011).wf 252 4194304 = true from a3.2)
  have a5 := FCat.wf_node.mp (show (FCat.node fcat62_n110110 fcat62_n110111).wf 252 4194304 = true from a4.2)
  have a6 := FCat.wf_node.mp (show (FCat.node fcat62_n1101110 fcat62_n1101111).wf 252 4194304 = true from a5.2)
  have a7 := FCat.wf_node.mp (show (FCat.node fcat62_n11011100 fcat62_n11011101).wf 252 4194304 = true from a6.1)
  have a8 := FCat.wf_node.mp (show (FCat.node fcat62_n110111000 fcat62_n110111001).wf 252 4194304 = true from a7.1)
  have a9 := FCat.wf_node.mp (show (FCat.node fcat62_n1101110000 fcat62_n1101110001).wf 252 4194304 = true from a8.1)
  have a10 := FCat.wf_node.mp (show (FCat.node fcat62_n11011100000 fcat62_r1083).wf 252 4194304 = true from a9.1)
  have b10 : fcatZ_n11011100001.wf 252 4194304 = true := FCat.wf_node.mpr ⟨a10.2, fcatZ_r3131_wf⟩
  have b9 : fcatZ_n1101110000.wf 252 4194304 = true := FCat.wf_node.mpr ⟨a10.1, b10⟩
  have b8 : fcatZ_n110111000.wf 252 4194304 = true := FCat.wf_node.mpr ⟨b9, a9.2⟩
  have b7 : fcatZ_n11011100.wf 252 4194304 = true := FCat.wf_node.mpr ⟨b8, a8.2⟩
  have b6 : fcatZ_n1101110.wf 252 4194304 = true := FCat.wf_node.mpr ⟨b7, a7.2⟩
  have b5 : fcatZ_n110111.wf 252 4194304 = true := FCat.wf_node.mpr ⟨b6, a6.2⟩
  have b4 : fcatZ_n11011.wf 252 4194304 = true := FCat.wf_node.mpr ⟨a5.1, b5⟩
  have b3 : fcatZ_n1101.wf 252 4194304 = true := FCat.wf_node.mpr ⟨a4.1, b4⟩
  have b2 : fcatZ_n110.wf 252 4194304 = true := FCat.wf_node.mpr ⟨a3.1, b3⟩
  have b1 : fcatZ_n11.wf 252 4194304 = true := FCat.wf_node.mpr ⟨b2, a2.2⟩
  have b0 : fcatZ_n1.wf 252 4194304 = true := FCat.wf_node.mpr ⟨a1.1, b1⟩
  exact FCat.wf_node.mpr ⟨a0.1, b0⟩

#print axioms fcatZ_wf
end CompactChecker
