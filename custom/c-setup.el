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


;; C-x`  or M-g M-n or M-g n  go to next error.
;; M-g p  or  M-g M-p   go to prev error
(add-hook 'c-mode-common-hook
          (lambda () (define-key c-mode-base-map (kbd "C-c C-c") 'compile)))

(add-hook 'c++-mode-common-hook
          (lambda () (define-key c++-mode-base-map (kbd "C-c C-c") 'compile)))


;; clang
(use-package clang-format
  :config
  (progn
    (global-set-key (kbd "C-c f") 'clang-format-region)
    (global-set-key (kbd "C-c u") 'clang-format-buffer)
    ;;(setq clang-format-style "file")
    ;;(setq clang-format-style "{BasedOnStyle: llvm, IndentWidth: 4, AccessModifierOffset: -4}")
   )
  )



(provide 'c-setup)
