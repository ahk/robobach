
// just a label with the name of the object

StringGui : ObjectGui {
	
	writeName {}
	gui { arg lay, bounds ... args;
		var layout,string,font;
		var width,height;
		layout=this.guify(lay,bounds);
		font = GUI.font.new(*GUI.skin.fontSpecs);
		if(model.isString,{
			string = " "++model;
		},{
			// floats, integers, symbols will show more clearly what they are
			string = " "++model.asCompileString;
		});		
		if(string.size > 1024,{
			string = string.copyRange(0,1024) ++ "...";
		});
		if(bounds.notNil,{
			bounds = bounds.asRect;
		},{
			bounds = Rect(0,0,
						string.bounds.width(font).max(30),
						// String(string.size * 7.0).max(70),
						GUI.skin.buttonHeight);
		});
		//[layout,layout.bounds,bounds].debug(string);
		this.view = GUI.staticText.new(layout,bounds)
			.stringColor_(GUI.skin.fontColor)//Color.black
			.font_(font)
			.background_(GUI.skin.background)//Color.white
			.align_(\left)
			.object_(string);

		if(lay.isNil,{ layout.resizeToFit(center:true).front });
	}

}


