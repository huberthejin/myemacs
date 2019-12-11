;; Ivy: is completion frameworks, like helm and ido.
;; Swiper: search through emacs and shows you text aroudn the matching terms.

(use-package ivy
  :init
  (progn
    (ivy-mode 1)
    (setq ivy-use-virtual-buffers t)
    (setq ivy-count-format "(%d/%d) ")
    (global-set-key (kbd "C-c s") 'swiper)
    ;(global-set-key (kbd "C-s") 'swiper)
    ))

(use-package counsel
  :bind
  (("M-x" . counsel-M-x)
   ("M-y" . counsel-yank-pop)
   ("C-c r" . counsel-recentf)
   ("C-x C-f" . counsel-find-file)
   ("<f1> f" . counsel-describe-function)
   ("<f1> v" . counsel-describe-variable)
   ("<f1> l" . counsel-load-library)
   ("C-h f" . counsel-describe-function)
   ("C-h v" . counsel-describe-variable)
   ("C-h l" . counsel-load-library)))

(use-package counsel-projectile
  :init
  (counsel-projectile-mode))

(provide 'ivy-counsel-setup)
