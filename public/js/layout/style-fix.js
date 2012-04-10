/**
 * Created by PyCharm.
 * User: PiVo
 * Date: 10.04.12
 * Time: 22:42
 * To change this template use File | Settings | File Templates.
 */
window.onload = function() {
	var isMSIE = '\v' == 'v';
	if (isMSIE) {
		var isResized = false;
		if (screen.systemXDPI === undefined) { //ie < 8
			var rect = document.body.getBoundingClientRect();
			isResized = (rect.right - rect.left) != document.body.clientWidth;
		} else { //ie > 7
			isResized = 96 != screen.deviceXDPI;
		}
		if (isResized) {
			var style_node = document.createElement("style");
			style_node.setAttribute("type", "text/css");
			style_node.setAttribute("media", "screen");

			if (document.styleSheets && document.styleSheets.length > 0) {
				var last_style_node = document.styleSheets[document.styleSheets.length - 1];
				if (typeof(last_style_node.addRule) == "object") {
					last_style_node.addRule('.background', 'filter: none !important;');
				}
			}
		}
	}
};