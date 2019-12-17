(use-package xcscope
  :config
  (progn
    ;; Always enbable cscope.
    (cscope-setup)
    (define-key global-map [(ctrl f3)] 'cscope-history-forward-line-current-result)
    (define-key global-map [(ctrl f4)] 'cscope-history-backward-line-current-result)

    ;; cscope-setup is not working for whatever reason, so I just add the ones that I need.
    ;;(global-set-key (kbd "C-c s s") 'cscope-find-this-symbol)
    ;;(global-set-key (kbd "C-c s t") 'cscope-find-this-text-string)
    ;;(global-set-key (kbd "C-c s e") 'cscope-find-egrep-pattern)
    )
  )




(provide 'xcscope-setup)
