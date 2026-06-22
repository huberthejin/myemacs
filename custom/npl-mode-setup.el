;;; npl-mode-setup.el --- Load and associate npl-mode  -*- lexical-binding: t; -*-

;;; Commentary:
;; Loads the local `npl-mode' and routes `.npl' files to it instead of
;; `p4-ts-mode'.
;;
;; npl-mode.el is Cisco-confidential (its keyword lists describe internal NPL)
;; and is therefore NOT committed to this (public) Emacs config repo.  The
;; canonical copy lives outside the repo -- in the private docs knowledge base
;; (docs/tools/npl-mode.el) or under ~/usr.  On startup, if a working copy is
;; missing from this directory (e.g. after `git clean'), it is seeded by copying
;; from the first candidate in `npl-mode-source-candidates' that exists.
;;
;; This file itself contains no NPL terms and is safe to commit.

;;; Code:

(require 'seq)

(defvar npl-mode-local-file
  (expand-file-name "npl-mode.el"
                    (file-name-directory (or load-file-name buffer-file-name
                                             default-directory)))
  "Path where the working copy of npl-mode.el is kept for `require'.")

(defvar npl-mode-source-candidates
  (list "/nobackup/hubjin/repo/docs/tools/npl-mode.el"
        (expand-file-name "~/usr/share/emacs/site-lisp/npl-mode.el"))
  "Ordered out-of-repo locations to seed npl-mode.el from.
The file is confidential and not committed here; edit this list if the
canonical copy moves.")

(defun npl-mode-ensure-installed ()
  "Ensure `npl-mode-local-file' exists, copying it from a known source.
Return non-nil when the file is present afterwards."
  (unless (file-exists-p npl-mode-local-file)
    (let ((src (seq-find #'file-exists-p npl-mode-source-candidates)))
      (if src
          (condition-case err
              (progn
                (copy-file src npl-mode-local-file t)
                (message "npl-mode: seeded %s from %s" npl-mode-local-file src))
            (error
             (display-warning
              'npl-mode
              (format "Failed to seed npl-mode.el from %s: %s"
                      src (error-message-string err)))))
        (display-warning
         'npl-mode
         (format "npl-mode.el not found locally and no source available.\nTried:\n  %s"
                 (mapconcat #'identity npl-mode-source-candidates "\n  "))))))
  (file-exists-p npl-mode-local-file))

(when (npl-mode-ensure-installed)
  (add-to-list 'load-path (file-name-directory npl-mode-local-file))
  (require 'npl-mode)
  (add-to-list 'auto-mode-alist '("\\.npl\\'" . npl-mode)))

(provide 'npl-mode-setup)
;;; npl-mode-setup.el ends here
