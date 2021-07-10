
(use-package multiple-cursors)

;; When you have an active region that spans multiple lines, the following will add a cursor to each line:
;; Ctrl-Shift-c
(global-set-key (kbd "C-S-c C-S-c") 'mc/edit-lines)


;; When you want to add multiple cursors not based on continuous lines, but based on keywords in the buffer
(global-set-key (kbd "C->") 'mc/mark-next-like-this)
(global-set-key (kbd "C-<") 'mc/unmark-next-like-this)
(global-set-key (kbd "C-M-<") 'mc/mark-previous-like-this)
(global-set-key (kbd "C-M->") 'mc/unmark-previous-like-this)

(defvar mc--insert-fancy-numbers-increment 1)
(defvar mc--insert-fancy-numbers-format "%d")

(defun mc/insert-fancy-numbers (start step format)
  "Insert increasing numbers for each cursor, starting from START,
counting by STEP and formatting them with the FORMAT specifier."
  (interactive "nStarting number: \nnIncrement: \nsFormat specifier (RET for '%%d'): ")
  (setq mc--insert-numbers-number start)
  (setq mc--insert-fancy-numbers-increment step)
  (setq mc--insert-fancy-numbers-format
        (if (string= format "") "%d" format))
  (mc/for-each-cursor-ordered
   (mc/execute-command-for-fake-cursor 'mc--insert-fancy-number-and-increase cursor)))

(defun mc--insert-fancy-number-and-increase ()
  (interactive)
  (insert (format mc--insert-fancy-numbers-format mc--insert-numbers-number))
  (setq mc--insert-numbers-number
        (+ mc--insert-numbers-number mc--insert-fancy-numbers-increment)))


(provide 'multiple-cursors-setup)
