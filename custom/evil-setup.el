
(use-package evil)

(evil-mode 1)

;; the following keys are bound to helm.
(define-key evil-normal-state-map (kbd "M-.") nil)
(define-key evil-normal-state-map (kbd "M-,") nil)

;; https://www.w3.org/wiki/CSS/Properties/color/keywords 

;; Color the evil tag - colors taken from spaceline
(setq evil-normal-state-tag   (propertize " <N> " 'face '((:background "DarkGoldenrod2" :foreground "black")))
      evil-emacs-state-tag    (propertize " <E> " 'face '((:background "SkyBlue2"       :foreground "black")))
      evil-insert-state-tag   (propertize " <I> " 'face '((:background "chartreuse3"    :foreground "black")))
      evil-replace-state-tag  (propertize " <R> " 'face '((:background "chocolate"      :foreground "black")))
      evil-motion-state-tag   (propertize " <M> " 'face '((:background "plum3"          :foreground "black")))
      evil-visual-state-tag   (propertize " <V> " 'face '((:background "gray"           :foreground "black")))
      evil-operator-state-tag (propertize " <O> " 'face '((:background "sandy brown"    :foreground "black"))))

(setq evil-default-cursor       '("DodgerBlue1" box)
      evil-normal-state-cursor  '("darkseagreen" box)
      evil-emacs-state-cursor   '("orange" box)
      evil-motion-state-cursor  '("SeaGreen1" box)
      evil-insert-state-cursor  '("black" bar)
      evil-visual-state-cursor  '("black" hbar)
      evil-replace-state-cursor '("pink" hbar))

(provide 'evil-setup)
