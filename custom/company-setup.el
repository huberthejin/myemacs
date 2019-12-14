
;; company: compete with auto-complete.
(use-package company
  :config
  (global-company-mode 1)
                                        ;(delete 'company-semantic company-backends))
  (setq company-backends (delete 'company-semantic company-backends))
  (setq company-dabbrev-downcase 0)
  (setq company-idle-delay 0)
  )







(provide 'company-setup)
