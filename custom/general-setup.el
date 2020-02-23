

(defun get-help ()
  (interactive)
  (message "*******************")
  (message "C-x C-j          use dired-jump")
  (message "C-x z            repeat commands, hit z to keep repeating.")
  (message "C-M-a	         Go to beginning of a function definition")
  (message "C-M-e	         Go to end of a function definition")
  (message "C-M-h	         Put a region around a function definition")
  (message "C-M-j            comment-indent-new-line, make next line comment.")
  (message "M-;              turn existing line into comments.")
  (message "M-x              comment-region")
  (message "mc/insert-numbers    to increase number across lines.")
  (message "Use C-u 1 M-x    mc/insert-numbers to increase number from 1.")
  (message "C-M-f =          forward-sexp    dash and underscore will be part of the word.")
  (message "C-M-b =          backward-sexp")
  (message "C-M-v and C-M-V  scroll the other windown.")
  (message "C-M-\\           indent the whole region")
  (message "C-M-n  C-M-p     Jump between parenthesis.")
  (message "C-h a mode       search all commands that has mode.")
  (message "C-h              which-key window")
  (message "C-x h            select all")
  (message "C-u C-<SPc>      twice  move back to original position.")
  (message "M-%%             query-replace.")
  (message "M-j              join line.")
  (message "C-`              yasnippet expand")
  (message "f5               save all buffers.")
;;  (message "f5               compilation")
  (message "C-c w            whitespace on/off")
  (message "C-c C-v          quick copy line")
  (message "C-c C-x          quick cut line")
  (message "C-return         open line below.")
  (message "C-S-return       open line up.")
  (message "M-g M-g          go to line.")
  (message "M-s              avy-goto-char")
  (message "C-c C-c          compile c/c++")
  (message "C-c f            clang-format-region")
  (message "C-c u            clang-format-buffer")
  (message "C-c C-j          semantic-ia-fast-jump")
  (message "C-c C-s          semantic-ia-show-summary")
  (message "[(ctrl f3)]      cscope-history-forward-line-current-result)")
  (message "[(ctrl f4)]      cscope-history-backward-line-current-result)")
  (message "M-;              comment-dwim-2")
  (message "M-%%             anzu-query-replace")
  (message "C-M-%%           anzu-query-replace-regexp")
  (message "C-x n n          narrow")
  (message "C-x n w          widen")
  (message "C-x n d          fuction.")
  (message "C-;              iedit-mode")
  (message "C-=              er/expand-region")
  (message "C--              er/contract-region")
  (message "M-<up arrow>     move current line/region up.")
  (message "M-<down arrow>   move current line/region down.")
  (message "C-x C-x          exchange-point-and-mark.")
  (message "C-x r y          exit multiple-cursor (enter) and while in new buffer hit C-x r y")
                                        ;(message " C-S-c C-S-c  mc/edit-lines)")"
  (message "C->              mc/mark-next-like-this")
  (message "C-<              mc/mark-previous-like-this")
  (message "C-c C-<          mc/mark-all-like-this")
  (message "C-c g s          ggtags-find-other-symbol")
  (message "C-c g h          ggtags-view-tag-history")
  (message "C-c g r          ggtags-find-reference")
  (message "C-c g f          ggtags-find-file")
  (message "C-c g c          ggtags-create-tags")
  (message "C-c g u          ggtags-update-tags")
  (message "C-c g a          helm-gtags-tags-in-this-function")
  (message "M-.              ggtags-find-tag-dwim")
  (message "M-,              pop-tag-mark")
  (message "C-c <            ggtags-prev-mark")
  (message "C-c >            ggtags-next-mark")
  (message "C-c g a          helm-gtags-tags-in-this-function")
  (message "C-j              helm-gtags-select")
  (message "M-.              helm-gtags-dwim")
  (message "M-,              helm-gtags-pop-stack")
  (message "C-c <            helm-gtags-previous-history")
  (message "C-c >            helm-gtags-next-history")

  (message "C-c C-f          next item in ag results")
  (message "C-c a a          ag")
  (message "C-c a d          ag-project-dired")
  (message "C-c a f          ag-project-files")
  (message "C-c a p          ag-project")
  (message "C-c a r          ag-project-regexp")

  (message "*******************") )




;;(menu-bar-mode -1)
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
;; use dired-jump   C-x C-j
(require 'dired-x)

(require 'org-setup)
(require 'dired-narrow-setup)

;; C-x  then wait couple of seconds.
(require 'which-key-setup)
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

(require 'ag-setup)
(require 'wgrep-setup)
(require 'wgrep-ag-setup)

(require 'rainbow-delimiters-setup)


;; ==========complete ways ======
;; 1. completion old way
(require 'xcscope-setup)
;;(require 'auto-complete-setup)
(require 'semantic-setup)

;; 2. complete with irony
;;(require 'completeirony-setup)



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
(require 'dumb-jump-setup)
(require 'rg-setup)
;;(require 'sr-speedbar-setup)

;; tabbar
;;(use-package tabbar
;;  :config (tabbar-mode 1) )

;; use Shirf and arrow key to move between windows
(windmove-default-keybindings)

;; Compilation
(global-set-key (kbd "<f8>") (lambda ()
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

;; find a specific file in specific directory.
(global-set-key (kbd "C-x f") 'find-name-dired)

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

(global-set-key [f5] 'my-save-some-buffers)

;; Reload file by force.
(defun revert-file ()
  "Revert buffer without confirmation."
  (interactive)
  (revert-buffer :ignore-auto :noconfirm))

;; Close all other buffers. Only keep the current one.
(defun kill-other-buffers ()
  "Kill all other buffers."
  (interactive)
  (mapc 'kill-buffer (delq (current-buffer) (buffer-list))))

;; Close all buffers.
(defun kill-all-buffers ()
  (interactive)
  (mapc 'kill-buffer (buffer-list)))

;; Change the face of code in #if 0 ...#endif block to comment face.
(defun my-c-mode-font-lock-if0 (limit)
  (save-restriction
    (widen)
    (save-excursion
      (goto-char (point-min))
      (let ((depth 0) str start start-depth)
        (while (re-search-forward "^\\s-*#\\s-*\\(if\\|else\\|endif\\)" limit 'move)
          (setq str (match-string 1))
          (if (string= str "if")
              (progn
                (setq depth (1+ depth))
                (when (and (null start) (looking-at "\\s-+0"))
                  (setq start (match-end 0)
                        start-depth depth)))
            (when (and start (= depth start-depth))
              (c-put-font-lock-face start (match-beginning 0) 'font-lock-comment-face)
              (setq start nil))
            (when (string= str "endif")
              (setq depth (1- depth)))))
        (when (and start (> depth 0))
          (c-put-font-lock-face start (point) 'font-lock-comment-face)))))
  nil)

(defun my-c-mode-common-hook ()
  (font-lock-add-keywords
   nil
   '((my-c-mode-font-lock-if0 (0 font-lock-comment-face prepend))) 'add-to-end))

(add-hook 'c-mode-common-hook 'my-c-mode-common-hook)




(provide 'general-setup)
