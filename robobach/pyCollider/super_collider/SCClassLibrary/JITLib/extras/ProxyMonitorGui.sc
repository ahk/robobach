
ProxyMonitorGui { 

	var <win, <zone, <flow;
	
		makeWatcher=true, skin| 
		
			.proxy_(proxy); 
		if (proxy.isNil or: proxy.isKindOf(NodeProxy)) {
			proxy = inproxy; 
			this.updateAll;
		} { 
			warn("ProxyMonitorGui: % is not a nodeproxy.".format(inproxy))
		};
	}
	
		var font; 
		var nameWid = 60; 
		var playWid = 34; 
		var outWid = 20; 
		var playNWid = 20;
		var pausSendWid = playWid * 2;
		var defaultBounds = 400@20;
		var height; 
		var widthSum, sliderWidth, winBounds, viewBounds;

		skin = skin ? GUI.skins.jit;
					
		usesPlayN = showPlayN; 
		usesName = showName;
		bounds = bounds ? defaultBounds; 
				
		if (w.notNil) { 
			win = w;
			viewBounds = bounds ? defaultBounds;
		} { 
			viewBounds = bounds;
			if (bounds.isKindOf(Point)) { 
				winBounds = Rect(80,400,0,0).setExtent(bounds.x, bounds.y);
			} { 
				winBounds = bounds; 
			};
		//	[\winBounds, winBounds, \viewBounds, 	viewBounds].postln; 
			win = Window(this.class.name.asString, winBounds, false).front;
		};
		
		
		
		if (viewBounds.isKindOf(Rect)) { viewBounds = viewBounds.extent };
		 
	//	[\bounds, bounds, \winBounds, winBounds, \viewBounds, viewBounds].postln;
		widthSum = 
			(showName.binaryValue * nameWid)
			+ playWid + outWid 
			+ (showPlayN.binaryValue * playNWid)
			+ (showPauseSend.binaryValue * pausSendWid);
		sliderWidth = viewBounds.x - widthSum; 

		height = viewBounds.y; 
		
			{ arg slid; 
				if(proxy.notNil) { 
					proxy.vol_(slid.value.dbamp); 
				} 
			}, 0, false, 
			labelWidth: showLevel.binaryValue * 20, 
			numberWidth: showLevel.binaryValue * 40);
		ampSl.labelView.font_(font).align_(0);
		
				
		
				[ \stop, skin.fontColor, skin.onColor ]
			]);
			
				// modifier alt should be elsewhere!!!
			// 524576 is alt, 262401 is ctl, 8388864 is fn
			// swingosc: 16 is normal  24 is alt, ctl is off, and fn is 16 as well
			var isAlt = [524576, 24].includes(modif); 
						if (usesPlayN) { proxy.playN } { proxy.play } 
					}
			{ |box, mod| 
				if (proxy.notNil) { 
					if (proxy.monitor.isNil) {  
						"ProxyMonitorGui - cant set outs yet.".postln 
					} { 
					};
				};
			
		setOutBox.numberView.font_(font).align_(0);

		if (usesPlayN) { 
				.font_(font)
					["-<", skin.fontColor, skin.onColor]
				.action_({ |box, mod|
					box.value_(1 - box.value);
		
		if (usesName) { 
			nameView = DragBoth(zone, Rect(0,0, nameWid, height));
			nameView.font_(font).align_(0)
				.setBoth_(false)
				.receiveDragHandler = { this.proxy_(View.implClass.currentDrag) };
		};
		
		if (usesPausSend) {
				.font_(font)
				.action_({ arg btn; 
				.font_(font)
				//	mod.postln;
						// alt-click osx, swingosc
					btn.value_(1 - btn.value)
		};
		 
		var currVol=0, pxname='<no proxy>', isAudio=false, plays=0, playsSpread=false, pauses=0, canSend=0; 
		
		
		
			canSend = proxy.objects.notEmpty.binaryValue;
			
			isAudio = proxy.rate == \audio;
			plays = monitor.isPlaying.binaryValue;
			
			if (monitor.notNil, { 
				playsSpread = proxy.monitor.hasSeriesOuts.not;
		} { 
			
		};
		
		currState = [currVol, pxname, isAudio, plays, outs, playsSpread, pauses, canSend];
		
		if (currState != oldState) { 
		//	"ProxyMonitorGui - updating.".postln; 
			if (currVol.notNil) { ampSl.value_(currVol.ampdb) };
			if (usesName) { nameView.object_(proxy).string_(pxname) };
			
			playBut.value_(plays);
			if (usesPausSend) { 
				pauseBut.value_(pauses);
				sendBut.value_(canSend);
			};
			
			if (isAudio != oldState[2]) { 
				[ampSl, playBut, setOutBox, playNDialogBut].reject(_.isNil).do(_.enabled_(isAudio));
			}; 
				// dont update if typing into numberbox - should be tested with SwingOSC!
			if (setOutBox.numberView.hasFocus.not) {	 
				setOutBox.value_(try { outs[0] } ? 0);
				if (usesPlayN) { 
					playNDialogBut.value_(playsSpread.binaryValue)
				};
			}
		};
		oldState = currState;