;; The themes are intended to be used with GUI
(setq custom--inhibit-theme-enable nil)

(use-package gruvbox-theme
  :config
;;  (load-theme 'gruvbox-dark-medium t)
;;  (load-theme 'gruvbox-dark-soft t)
  (load-theme 'gruvbox-dark-hard t)
;;  (load-theme 'gruvbox-light-soft t)
;;  (load-theme 'alect-dark-alt t)
;;  (load-theme 'alect-black t)
;;  (load-theme 'alect-black-alt t)
  )

(custom-theme-set-faces
     'gruvbox
     '(region   ((t (:background "#c0c000" ))))
     '(highlight   ((t (:background "#7f400b" :foreground "#f0f0f0")))))


(provide 'gruvbox-themes-setup)
