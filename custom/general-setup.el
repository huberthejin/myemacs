;; C-M-j  comment-indent-new-line, make next line comment.
;; M-;    turn existing line into comments.
;; M-x comment-region

;; Use  mc/insert-numbers to increase number across lines.
;; Use C-u 1 M-x mc/insert-numbers to increase number from 1.
;; C-M-f = forward-sexp    dash and underscore will be part of the word.
;; C-M-b = backward-sexp
;; C-M-v and C-M-V  scroll the other windown.
;; C-M-\  indent the whole region
;; C-M-n  C-M-p   Jump between parenthesis.
;; C-h a mode   search all commands that has mode.
;; C-x h  select all
;; M-%  query-replace.
;; M-j  join line.
;; C-`  yasnippet expand
;; f1 save all buffers.
;; f5  compilation
;; C-c w  whitespace on/off
;; C-c C-v quick copy line
;; C-c C-x quick cut line
;; C-S-down   move line down
;; C-S-up     move line up.
;; C-return   open line below.
;; C-S-return open line up.
;; M-g M-g    go to line.
;; M-s        avy-goto-char
;; C-c C-c    compile c/c++
;; C-c f      clang-format-region
;; C-c u      clang-format-buffer
;; C-c C-j    semantic-ia-fast-jump
;; C-c C-s    semantic-ia-show-summary
;; [(ctrl f3)] cscope-history-forward-line-current-result)
;; [(ctrl f4)] cscope-history-backward-line-current-result)
;; M-;         comment-dwim-2
;; M-%         anzu-query-replace
;; C-M-%       anzu-query-replace-regexp
;; C-x n n     narrow
;; C-x n w     widen
;; C-x n d     fuction.
;; C-;"        iedit-mode
;; C-=         er/expand-region)
;; C--         er/contract-region)
;; M-<up arrow>  move current line up.
;; M-<down arrow>  move current line down.
;; C-x C-x     exchange-point-and-mark.
;; C-x r y      exit multiple-cursor (enter) and while in new buffer hit C-x r y


;; C-S-c C-S-c    mc/edit-lines)
;; C->            mc/mark-next-like-this)
;; C-<            mc/mark-previous-like-this)
;; C-c C-<        mc/mark-all-like-this)

;; C-c g s"    ggtags-find-other-symbol)
;; C-c g h"    ggtags-view-tag-history)
;; C-c g r"    ggtags-find-reference)
;; C-c g f"    ggtags-find-file)
;; C-c g c"    ggtags-create-tags)
;; C-c g u"    ggtags-update-tags)
;; C-c g a"    helm-gtags-tags-in-this-function)
;; M-.         ggtags-find-tag-dwim)
;; M-,         pop-tag-mark)
;; C-c <       ggtags-prev-mark)
;; C-c >       ggtags-next-mark)

;; C-c g a     helm-gtags-tags-in-this-function)
;; C-j         helm-gtags-select)
;; M-.         helm-gtags-dwim)
;; M-,         helm-gtags-pop-stack)
;; C-c <       helm-gtags-previous-history)
;; C-c >       helm-gtags-next-history))))










(menu-bar-mode -1)
(tool-bar-mode -1)

;;size of garbage collector.
(setq gc-cons-threshold 100000000)

;; disable splash screen and startup messages.
(setq inhibit-splash-screen t)
(setq inhibit-startup-message t)

;; y or n is enough
(defalias 'yes-or-no-p 'y-or-n-p)

;; show unncessary whitespace that can mess up your diff
(add-hook 'prog-mode-hook
          (lambda () (interactive)
            (setq show-trailing-whitespace 1)))

;; use space to indent by default
(setq-default indent-tabs-mode nil)

;; set appearance of a tab that is represented by 4 spaces
(setq-default tab-width 4)

;; Open buffer in current window, not the other window(by default).
;(global-set-key "\C-x\C-b" 'buffer-menu)
(global-set-key "\C-x\C-b" 'ibuffer)

;; Now hashfiles
(setq create-lockfiles nil)

;; No backup files
(setq make-backup-files nil)

;; Display line number on side
;;(global-linum-mode t)

;; Auto-refresh all buffers when files have changes on disk.
(global-auto-revert-mode t)

;; Load large TAGS file
(setq large-file-warning-threshold nil)

;; after copy Ctrl+c in Linux X11, you can paste by `yank' in emacssgdefggtrfdesffsfdf
(setq x-select-enable-clipboard t)

;; after mouse selection in X11, you can paste by `yank' in emacs
(setq x-select-enable-primary t)

;; show matching parenthesis
(show-paren-mode 1)

;; cursor jitter issue.
(setq auto-window-vscroll nil)

;; join lines
(global-set-key (kbd "M-j") (lambda ()(interactive)(join-line -1)) )

;; Always follow the symlink
(setq vc-follow-symlinks t)

;; Replace the active region just by typing text, and delete the
;; selected text just by hitting the Backspace key.
(delete-selection-mode 1)

(put 'narrow-to-region 'disabled nil)

(setq c-default-style "linux"
      c-basic-offset 4)








;;;; ============= Individual setting above this line ===========

;; C-x  then wait couple of seconds.
;;(use-package which-key
;;  :config (which-key-mode))
(require 'helm-setup)
(require 'helm-gtags-setup)

(require 'uniquify-setup)
(require 'yasnippet-setup)
(require 'smartparens-setup)
(require 'avy-setup)
(require 'expand-region-setup)
(require 'protobuf-setup)
(require 'cmake-setup)
(require 'column-indicator-setup)
(require 'magit-setup)
(require 'company-setup)
(require 'projectile-setup)
(require 'zygospore-setup)
(require 'gdb-setup)
;; (require 'ggtags-setup)
(require 'c-setup)
(require 'cedet-setup)
;;(require 'editing-setup)
(require 'multiple-cursors-setup)
(require 'move-text-setup)

;; ==========complete ways ======
;; 1. completion old way
(require 'xcscope-setup)
;;(require 'auto-complete-setup)
(require 'semantic-setup)

;; 2. complete with irony
(require 'completeirony-setup)



;;(require 'flycheck-setup)

;; *************editing related **********

(require 'volatile-highlights-setup)
(require 'undo-tree-setup)
(require 'clean-aindent-mode-setup)
;;(require 'dtrt-indent-setup)
(require 'ws-butler-setup)
(require 'comment-dwin-2-setup)
(require 'anzu-setup)
(require 'iedit-setup)

;; tabbar
;;(use-package tabbar
;;  :config (tabbar-mode 1) )

;; use Shirf and arrow key to move between windows
(windmove-default-keybindings)

;; Compilation
(global-set-key (kbd "<f5>") (lambda ()
                               (interactive)
                               (setq-local compilation-read-command nil)
                               (call-interactively 'compile)))

(setq
 ;; use gdb-many-windows by default
 gdb-many-windows t
 ;; Non-nil means display source file containing the main routine at startup
 gdb-show-main t
 )




;; automatically indent when press RET

;; activate whitespace-mode to view all whitespace characters
(global-set-key (kbd "C-c w") 'whitespace-mode)
(windmove-default-keybindings)




;; ***************** define my own functions here **********************

(defun quick-copy-line ()
  "Copy the whole line that point is on and move to the beginning of the next line.
    Consecutive calls to this command append each line to the
    kill-ring."
  (interactive)
  (let ((beg (line-beginning-position 1))
        (end (line-beginning-position 2)))
    (if (eq last-command 'quick-copy-line)
        (kill-append (buffer-substring beg end) (< end beg))
      (kill-new (buffer-substring beg end))))
  (beginning-of-line 2))
(global-set-key "\C-c\C-v" 'quick-copy-line)


(defun quick-cut-line ()
  "Cut the whole line that point is on.  Consecutive calls to this command append each line to the kill-ring."
  (interactive)
  (let ((beg (line-beginning-position 1))
        (end (line-beginning-position 2)))
    (if (eq last-command 'quick-cut-line)
        (kill-append (buffer-substring beg end) (< end beg))
      (kill-new (buffer-substring beg end)))
    (delete-region beg end))
  (beginning-of-line 1)
  (setq this-command 'quick-cut-line))
(global-set-key "\C-c\C-x" 'quick-cut-line)


;; Move current line up or down one line.
(defun move-line-down ()
  (interactive)
  (let ((col (current-column)))
    (save-excursion
      (forward-line)
      (transpose-lines 1))
    (forward-line)
    (move-to-column col)))

(defun move-line-up ()
  (interactive)
  (let ((col (current-column)))
    (save-excursion
      (forward-line)
      (transpose-lines -1))
    (forward-line -1)
    (move-to-column col)))

(global-set-key (kbd "<C-S-down>") 'move-line-down)
(global-set-key (kbd "<C-S-up>") 'move-line-up)



;; Add an empbly line below or above current line.
(defun open-line-below ()
  (interactive)
  (end-of-line)
  (newline)
  (indent-for-tab-command))

(defun open-line-above ()
  (interactive)
  (beginning-of-line)
  (newline)
  (forward-line -1)
  (indent-for-tab-command))
(global-set-key (kbd "<C-return>") 'open-line-below)
(global-set-key (kbd "<C-S-return>") 'open-line-above)

(global-set-key [remap goto-line] 'goto-line-with-feedback)

(defun goto-line-with-feedback ()
  "Show line numbers temporarily, while prompting for the line number input"
  (interactive)
  (unwind-protect
      (progn
        (linum-mode 1)
        (goto-line (read-number "Goto line: ")))
    (linum-mode -1)))


;; Treat underscore as part of word.
(add-hook 'after-change-major-mode-hook 'hj-treat-underscore-as-word-char)
(defun hj-treat-underscore-as-word-char ()
  (progn
    (modify-syntax-entry ?_ "w")
    ;;(modify-syntax-entry ?- "w")
    ))

;; Save all the files
(defun my-save-some-buffers ()
  (interactive)
  (save-some-buffers 'no-confirm (lambda ()
                                   (cond
                                    ((and buffer-file-name (eq major-mode 'c-mode)))
                                    ((and buffer-file-name (eq major-mode 'c++-mode)))))))

(global-set-key [f1] 'my-save-some-buffers)

;; Reload file by force.
(defun revert-file ()
  "Revert buffer without confirmation."
  (interactive)
  (revert-buffer :ignore-auto :noconfirm))



(provide 'general-setup)
