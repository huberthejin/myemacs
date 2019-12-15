
;; PACKAGE: iedit
;; C-x n n : narrow
;; C-x n w : widen
;; C-x n d : fuction.
(use-package iedit
  :bind (("C-;" . iedit-mode))
  :init
  (setq iedit-toggle-key-default nil))


(provide 'iedit-setup)
