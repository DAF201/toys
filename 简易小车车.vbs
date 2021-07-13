set WshShell = WScript.CreateObject("WScript.Shell")
	WshShell.AppActivate " "
		for i=1 to 5
			WScript.Sleep 500
			WshShell.SendKeys "^v"
			WshShell.SendKeys "~"
			Next
