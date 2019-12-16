
;; yasnippet: create template.
(use-package yasnippet
  :init
  (progn
    (yas-global-mode 1)
    (define-key yas-minor-mode-map (kbd "TAB") nil)
    (define-key yas-minor-mode-map (kbd "<tab>") nil)
    ;;(define-key yas-minor-mode-map (kbd "<C-tab>") #'yas-expand)
    (define-key yas-minor-mode-map (kbd "C-`") #'yas-expand)
    )
  :config
  ;;(add-to-list 'yas-snippet-dirs (expand-file-name "~/.emacs.d/custom/snippets"))
  (use-package yasnippet-snippets
    :config
    (progn
      (add-to-list 'load-path "~/.emacs.d/elpa/yasnippet-snippets-20190926.1252")
      (add-to-list 'load-path "~/.emacs.d/snippets") ; Add my own snippets here.
      )
    )
  )

;;(use-package yasnippet
;;  :defer t
;;  :init
;;  (add-hook 'prog-mode-hook 'yas-minor-mode))


(provide 'yasnippet-setup)
