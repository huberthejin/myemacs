
;; Activate next-error-follow-minor-mode with C-c C-f. 
;; Use C-h m inside a results buffer to show all available keybindings.

(use-package yaml-mode
  :config
  (progn
    ; To automatically handle files ending in '.yml'
    (add-to-list 'auto-mode-alist '("\\.yml\\'" . yaml-mode))
    )
  )
(add-hook 'yaml-mode-hook 'highlight-indent-guides-mode)


(provide 'yaml-setup)
