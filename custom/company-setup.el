
;; company: compete with auto-complete.
(use-package company
  :config
  (global-company-mode 1)
                                        ;(delete 'company-semantic company-backends))
  (setq company-backends (delete 'company-semantic company-backends))
  (setq company-dabbrev-downcase 0)
  (setq company-idle-delay 0)
 ;; (setq company-idle-delay 3)
  )

(defun sd/company-stop-input-space ()
  "Stop completing and input a space,a workaround of a semantic issue `https://github.com/company-mode/company-mode/issues/614'"
  (interactive)
  (company-abort)
  (insert " "))

(define-key company-active-map (kbd "SPC") #'sd/company-stop-input-space)





(provide 'company-setup)
