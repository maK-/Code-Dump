function js_compact(str)
{   /*
	 * whitespace surrounding these characters is unnecessary:
	 * {}()[]<>.;,=!+-*%&|^~?:"'/
	 */
	var js_compact_punctuation = '{}()\\[\\]<>.;,=!+\\-*%&|^~?:"\'\/';
	var idx, output = '', re_falsealarm, safe, type, hunt;
	/*
	 * js_compact_code:
	 * this function performs simple whitespace reduction, and assumes
	 * the spacing within the passed str isn't important
	 */
	function js_compact_code(str)
	{
		var re_whitespace;
		/* translate and reduce whitespace */
		str = str.replace(/\s+/g, ' ');
		/* remove leading/trailing whitespace */
		str = str.replace(/^ *(.*\S) *$/, '$1');
		/* remove unnecessary whitespace around punctuation */
		re_whitespace = new RegExp(' *([' + js_compact_punctuation + ']) *', 'g');
		str = str.replace(re_whitespace, '$1');
		return str;
	}

	/* paranoia */
	for (safe = 0; safe < 1024*1024; safe++) {
		/* look for a quote (", ', /, or /*) */
		if ((idx = str.search(/["'\/]/)) != -1) {
			/* store the quote type */
			type = str.charAt(idx);
		    /* check to see if this was a false alarm (non-regexp /) */
			if (type == '/') {
				re_falsealarm = new RegExp('[^' + js_compact_punctuation + ' \f\n\r\t\u00A0\u2028\u2029]+\s*' + type + '$');
				if (str.substr(0, idx + 1).search(re_falsealarm) != -1) {
					/* it's a false alarm, remove whitespace and continue */
					output += js_compact_code(str.substr(0, idx + 1));
					str = str.substr(idx + 1);
					continue;
				}
				/*
				 * comments are a special case because they look a lot
				 * like regexp literals :/
				 */
				if (str.charAt(idx + 1) == '*')
					type = '*/'
			}

			/* remove whitespace */
			output += js_compact_code(str.substr(0, idx));

			/* advance past unquoted text */
			str = str.substr(idx);

			/* look for closing quote */
			if (type == '*/') {
				hunt = '\\*/';
			} else {
				hunt = '[^\\\\]' + type;
			}
            /*
			 * the offset in the substrs below is 2 because the normal quote
			 * case matches an extra character (the non-\ char), but the
			 * comment case doesn't (comments can't be escaped), making
			 * the length for each match 2 chars.
			 */
			if ((idx = str.search(hunt)) != -1) {
				/* found it, so if it's not a comment... */
				if (type != '*/') {
					/* ...add quoted text verbatim */
					output += str.substr(0, idx + 2);
				}

				/* advance past the quoted section */
				str = str.substr(idx + 2);
			} else {
				/* abandon ship! */
				alert('Missing trailing ' + type + ':\n' + str);
				break;
			}
		} else {
			/* no more quotes, compact remainder */
			output += js_compact_code(str);
			break;
		}
	}
	return output;
}
