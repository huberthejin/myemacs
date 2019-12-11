(use-package irony
  :ensure t
  :hook ((c++-mode . irony-mode)
         (c-mode . irony-mode))
  :config
  (add-hook 'irony-mode-hook 'irony-cdb-autosetup-compile-options)
  (use-package company-irony-c-headers
    :ensure t)
  (use-package company-irony
    :ensure t
    :config
    (add-to-list (make-local-variable 'company-backends)
                 '(company-irony company-irony-c-headers)))

;; too many errors
;;  (use-package flycheck-irony
;;    :ensure t
;;    :config
;;    (add-hook 'flycheck-mode-hook #'flycheck-irony-setup)
;;    )

  (use-package irony-eldoc
    :ensure t
    :config
    (add-hook 'irony-mode-hook #'irony-eldoc)
    )
  )

(provide 'completeirony-setup)
