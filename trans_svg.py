#! encoding:UTF-8
import cairosvg
import os
 
#pip3 install cairosvg
 
 
# SVG转PNG
cairosvg.svg2png(file_obj=open("./svgs/1.svg", "rb"), write_to="./pngs/1.png")
# SVG转PDF
# cairosvg.svg2pdf( file_obj=open("E://svgFile//a.svg", "rb"), write_to="E://svgFile//a.pdf")
# # SVG转PS
# cairosvg.svg2ps(bytestring=open("E://svgFile//a.svg").read().encode('utf-8'))