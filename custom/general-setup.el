

;; ***************** define my own functions here **********************

;; find a specific file in specific directory.
(global-set-key (kbd "C-x f d") 'find-name-dired)

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
(global-set-key (kbd "C-c k o") 'kill-other-buffers)

;; Close all buffers.
(defun kill-all-buffers ()
  (interactive)
  (mapc 'kill-buffer (buffer-list)))
(global-set-key (kbd "C-c k a") 'kill-all-buffers)

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


(defun my-format-function ()
  (let* (
        (beg (line-beginning-position))
        (end (line-end-position))
        (retstr "0")
        )
    (save-excursion
      (save-restriction
        (narrow-to-region beg end)
        (goto-char(point-min))
        (while (search-forward "(" nil 1)
          (backward-char)
          (setq retstr "1")
          (if(not (char-equal ?\s (char-before)  ))
              (progn
                (insert " ")
                ;; return 1 change is already mad
                )
            )
            (forward-char)
          )
        )
      )
    retstr
    )
  )

(defun my-format-asterisk ()
  (let* (
         (beg (line-beginning-position))
         (end (line-end-position))
         (retstr "0")
         )
    (save-excursion
      (save-restriction
        (narrow-to-region beg end)
        (goto-char (point-min))
        (search-forward "*" nil 1)
        (setq startpos (point))
        (if (char-equal ?\s (char-after))
            ;;  one asterisk
            (progn
              ;;(forward-char)
              (while (char-equal ?\s (following-char))
                (forward-char)
                )
              (insert "*")
              (goto-char startpos)
              (delete-backward-char 1)
              )
          )
        )
      )
    retstr
    )
  )


(defun myformat ()
  (interactive)
  (setq retval (my-format-function))
  (if(string= retval "0")
      (my-format-asterisk)
    (message "done")
    )
  )

(global-set-key(kbd "C-c f c") 'myformat)


(defun forward-or-backward-sexp (&optional arg)
  "Go to the matching parenthesis character if one is adjacent to point."
  (interactive "^p")
  (cond ((looking-at "\\s(") (forward-sexp arg))
        ((looking-back "\\s)" 1) (backward-sexp arg))
        ;; Now, try to succeed from inside of a bracket
        ((looking-at "\\s)") (forward-char) (backward-sexp arg))
        ((looking-back "\\s(" 1) (backward-char) (forward-sexp arg))) )

(global-set-key(kbd "C-%") 'forward-or-backward-sexp)

;; emacsclient specific init
;; We set startup directory to current directory.
(defun init-emacsclient (&optional curdir)
  (interactive "^p")
  (with-current-buffer "*scratch*"
    (setq default-directory (concat curdir "/"))))

;;;;   int *              abc;

;;;; test_this_btest_boot (int i, int j


;; Fix "Unmatched Text during Lexical Analysis" error.
;;(advice-add 'semantic-idle-scheduler-function :around #'ignore)


(provide 'general-setup)
