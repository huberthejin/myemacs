;; company-c-headers
(use-package company-c-headers
  :init
  (add-to-list 'company-backends 'company-c-headers))

;; hs-minor-mode for folding source code
(add-hook 'c-mode-common-hook 'hs-minor-mode)

;; Available C style:
;; “gnu”: The default style for GNU projects
;; “k&r”: What Kernighan and Ritchie, the authors of C used in their book
;; “bsd”: What BSD developers use, aka “Allman style” after Eric Allman.
;; “whitesmith”: Popularized by the examples that came with Whitesmiths C, an early commercial C compiler.
;; “stroustrup”: What Stroustrup, the author of C++ used in his book
;; “ellemtel”: Popular C++ coding standards as defined by “Programming in C++, Rules and Recommendations,” Erik Nyquist and Mats Henricson, Ellemtel
;; “linux”: What the Linux developers use for kernel development
;; “python”: What Python developers use for extension modules
;; “java”: The default style for java-mode (see below)
;; “user”: When you want to define your own style
(setq c-default-style "linux"
      c-basic-offset 4)

(use-package cc-mode
  :ensure t
  :config ;:init
  (define-key c-mode-map  [(tab)] 'company-complete)
  (define-key c++-mode-map  [(tab)] 'company-complete))

(add-to-list 'auto-mode-alist '("\\.enumh\\'" . c-mode))
(add-to-list 'auto-mode-alist '("\\.enumc\\'" . c-mode))
(add-to-list 'auto-mode-alist '("\\.cp\\'" . c-mode))
(add-to-list 'auto-mode-alist '("\\.hp\\'" . c-mode))

;; Fix the issue that /** has different color
(defun my-cc-init-hook ()
  "Initialization hook for CC-mode runs before any other hooks."
  (setq c-doc-comment-style
    '((java-mode . javadoc)
      (pike-mode . autodoc)
      (c-mode    . javadoc)
      (c++-mode  . javadoc)))
  (set-face-foreground 'font-lock-doc-face
               (face-foreground font-lock-comment-face)))
(add-hook 'c-initialization-hook 'my-cc-init-hook)

(global-set-key (kbd "C-c C-c") nil)
;; C-x`  or M-g M-n or M-g n  go to next error.
;; M-g p  or  M-g M-p   go to prev error
;;(add-hook 'c-mode-common-hook
;;          (lambda () (define-key c-mode-base-map (kbd "C-c C-c") 'compile)))
;;
;;(add-hook 'c++-mode-common-hook
;;          (lambda () (define-key c++-mode-base-map (kbd "C-c C-c") 'compile)))



;; C-Like syntax highlighting
(dolist (mode-iter '(c-mode c++-mode glsl-mode java-mode javascript-mode rust-mode))
  (font-lock-add-keywords
    mode-iter
    '(("\\([~^&\|!<>=,.\\+*/%-]\\)" 0 'font-lock-operator-face keep)))
  (font-lock-add-keywords
    mode-iter
    '(("\\([\]\[}{)(:;]\\)" 0 'font-lock-delimit-face keep)))
  ;; functions
  (font-lock-add-keywords
    mode-iter
    '(("\\([_a-zA-Z][_a-zA-Z0-9]*\\)\s*(" 1 'font-lock-function-name-face keep))))


(require 'clang-setup)


(provide 'c-setup)
