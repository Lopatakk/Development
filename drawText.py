def drawText(surface, text, color, rect, font, align, aa=False, bkg=None):
    textAlignLeft = 0
    textAlignRight = 1
    textAlignCenter = 2
    textAlignBlock = 3

    lineSpacing = 5
    #   gets width and height of the font
    spaceWidth, fontHeight = font.size(" ")[0], font.size("Tq")[1]

    listOfWords = text.split(" ")   # splits words based on space
    if bkg: # background color of text
        imageList = [font.render(word, 1, color, bkg) for word in listOfWords]
        for image in imageList: image.set_colorkey(bkg)
    else: # None = no background color
        imageList = [font.render(word, aa, color) for word in listOfWords]  # creates a list (one line) of images using the render.font function, which converts text to an image

    maxLen = rect[2]
    lineLenList = [0]
    lineList = [[]]
    #   it goes through the entire row (line) of images and chops it according to maxLen
    for image in imageList:
        width = image.get_width()
        lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + width  #   lenght of line with images
        if len(lineList[-1]) == 0 or lineLen <= maxLen:
            lineLenList[-1] += width
            lineList[-1].append(image)
        else:
            lineLenList.append(width)
            lineList.append([image])

    lineBottom = rect[1]
    lastLine = 0
    for lineLen, lineImages in zip(lineLenList, lineList):
        lineLeft = rect[0]
        #   there is no left alignment here, as it is done in the base
        if align == textAlignRight:
            lineLeft += + rect[2] - lineLen - spaceWidth * (len(lineImages)-1)
        elif align == textAlignCenter:
            lineLeft += (rect[2] - lineLen - spaceWidth * (len(lineImages)-1)) // 2
        elif align == textAlignBlock and len(lineImages) > 1:
            spaceWidth = (rect[2] - lineLen) // (len(lineImages)-1)
        #   to limit the text to the bottom line of the rectangle
        # if lineBottom + fontHeight > rect[1] + rect[3]:
        #     break
        lastLine += 1
        #   rendering of text images on the specified surfaces specified above
        for i, image in enumerate(lineImages):
            x, y = lineLeft + i*spaceWidth, lineBottom
            surface.blit(image, (round(x), y))
            lineLeft += image.get_width()
        lineBottom += fontHeight + lineSpacing

    lowest = lineBottom - lineSpacing

    #   to draw the specified rectangle
    # pygame.draw.rect(surface, (255, 255, 255), rect, 1)

    return lowest