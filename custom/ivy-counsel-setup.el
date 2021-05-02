;; Ivy: is completion frameworks, like helm and ido.
;; Swiper: search through emacs and shows you text aroudn the matching terms.

(use-package ivy
  :init
  (progn
    (ivy-mode 1)
    (setq ivy-use-virtual-buffers t)
    (setq enable-recursive-minibuffers t)
;;    (global-set-key (kbd "C-z") 'swiper)
;;    (global-set-key (kbd "C-,") 'swiper-isearch)
    ))

;; The following select the word at cursor.
(defun ivy-with-thing-at-point (cmd)
  (let ((ivy-initial-inputs-alist
         (list
          (cons cmd (thing-at-point 'symbol)))))
    (funcall cmd)))

;; Example 1
(defun counsel-ag-thing-at-point ()
  (interactive)
  (ivy-with-thing-at-point 'counsel-ag))

;; swiper with word at the cursor
(defun swiper-thing-at-point ()
  (interactive)
  (ivy-with-thing-at-point 'swiper))

;; swiper-isearch with word at the cursor
(defun swiper-isearch-thing-at-point ()
  (interactive)
  (ivy-with-thing-at-point 'swiper-isearch))

(global-set-key (kbd "C-,") 'swiper-isearch-thing-at-point)
(global-set-key (kbd "C-z") 'swiper-thing-at-point)


(use-package counsel)
;;  :bind
;;  (("M-x" . counsel-M-x)
;;   ("M-y" . counsel-yank-pop)
;;   ("C-c r" . counsel-recentf)
;;   ("C-x C-f" . counsel-find-file)
;;   ("<f1> f" . counsel-describe-function)
;;   ("<f1> v" . counsel-describe-variable)
;;   ("<f1> l" . counsel-load-library)
;;   ("C-h f" . counsel-describe-function)
;;   ("C-h v" . counsel-describe-variable)
;;   ("C-h l" . counsel-load-library)))

;;(use-package counsel-projectile
;;  :init
;;  (counsel-projectile-mode))

(provide 'ivy-counsel-setup)
