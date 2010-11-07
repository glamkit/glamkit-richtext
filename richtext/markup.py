from template_utils.markup import formatter




def typogridown(text, **kwargs):
    from BeautifulSoup import BeautifulSoup
    from BeautifulSoup import BeautifulStoneSoup
    from typogrify.templatetags.typogrify import typogrify
    from markdown import markdown
    soup = BeautifulStoneSoup(unicode(text), convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    htmlized = typogrify(markdown(unicode(soup), extensions=kwargs.get('extensions', [])))
    soup = BeautifulSoup(htmlized)
    # This is ugly, but it's the easiest way to kill extraneous paragraphs Markdown inserts.
    return unicode(soup).replace('<p><div', '<div').replace('</div>\n\n</p>', '</div>\n\n')

formatter.register('typogridown', typogridown)







def typygmentdown(text, **kwargs):
    """
    Given a string of text using Markdown syntax, applies the
    following transformations:

    1. Searches out and temporarily removes any raw ``<code>``
       elements in the text.
    2. Applies Markdown and typogrify to the remaining text.
    3. Applies Pygments highlighting to the contents of the removed
       ``<code>`` elements.
    4. Re-inserts the ``<code>`` elements and returns the result.

    The Pygments lexer to be used for highlighting is determined by
    the ``class`` attribute of each ``<code>`` element found; if none
    is present, it will attempt to guess the correct lexer before
    falling back on plain text.

    The following keyword arguments are understood and passed to
    markdown if found:

    * ``extensions``

    Markdown's ``safe_mode`` argument is *not* passed on, because it
    would cause the temporary ``<code>`` elements in the text to be
    escaped.

    The following keyword arguments are understood and passed to
    Pygments if found:

    * ``linenos``

    The removal, separate highlighting and re-insertion of the
    ``<code>`` elements is necessary because Markdown and SmartyPants
    do not reliably avoid formatting text inside these elements;
    removing them before applying Markdown and typogrify means they
    are in no danger of having extraneous HTML or fancy punctuation
    inserted by mistake.

    Original implementation by user 'blinks' as snippet #119 at
    djangosnippets: http://www.djangosnippets.org/snippets/119/. This
    version makes the following changes:

    * The name of the function is now ``typygmentdown``.
    * The argument signature has changed to work better with the
      ``template_utils`` formatter.
    * The ``extensions`` and ``linenos`` arguments are looked for and
      passed to Markdown and Pygments, respectively.
    * The function is registered with the ``template_utils``
      formatter.

    """
    from BeautifulSoup import BeautifulSoup
    from BeautifulSoup import BeautifulStoneSoup
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from typogrify.templatetags.typogrify import typogrify
    from markdown import markdown
    soup = BeautifulStoneSoup(unicode(text), convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
    code_blocks = soup.findAll('code')
    for block in code_blocks:
        block.replaceWith('<code class="removed"></code>')
    htmlized = typogrify(markdown(unicode(soup), extensions=kwargs.get('extensions', [])))
    soup = BeautifulSoup(htmlized)
    empty_code_blocks, index = soup.findAll('code', 'removed'), 0
    formatter = HtmlFormatter(cssclass='typygmentdown', linenos=kwargs.get('linenos', False))
    for block in code_blocks:
        if block.has_key('class'):
            language = block['class']
        else:
            language = 'text'
        try:
            lexer = get_lexer_by_name(language, stripnl=True, encoding='UTF-8')
        except ValueError, e:
            try:
                lexer = guess_lexer(block.renderContents())
            except ValueError, e:
                lexer = get_lexer_by_name('text', stripnl=True, encoding='UTF-8')
        empty_code_blocks[index].replaceWith(
                '<div class="code-block">' + highlight(block.renderContents(), lexer, formatter) + '</div>')
        index = index + 1
    # I'll just leave this line here in case we ever need to define inline styles
    # Be sure to add a style='style_name' parameter to the formatter initialisation
    # The Pygments built-in styles that are light-on-dark are 'fuity' and 'native'
    #style = u'<style>%s</style>' % formatter.get_style_defs()
    # This is ugly, but it's the easiest way to kill extraneous paragraphs Markdown inserts.
    return unicode(soup).replace('<p><div', '<div').replace('</div>\n\n</p>', '</div>\n\n')

formatter.register('typygmentdown', typygmentdown)
