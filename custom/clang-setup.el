;; clang
(use-package clang-format
  :config
  (progn
    (global-set-key (kbd "C-c f f") 'clang-format-region)
;;;    (global-set-key (kbd "C-c u") 'clang-format-buffer)
    ;;(setq clang-format-style "file")
    ;;(setq clang-format-style "{BasedOnStyle: llvm, IndentWidth: 4, AccessModifierOffset: -4}")
    )
  )

;; clang+
;; Used for format during save disabled for now
;;(use-package clang-format+
;;  :config
;;  (progn
;;    (add-hook 'c-mode-common-hook #'clang-format+-mode))
;;    (setq clang-format+-context 'modification)
;;  )

(provide 'clang-setup)
