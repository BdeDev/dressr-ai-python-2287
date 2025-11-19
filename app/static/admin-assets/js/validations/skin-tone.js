$("#add-skin-tones").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
        color_code: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
        color_code: {
			required: "Please Enter Colour Code",
			},
        }
	});  


$("#edit-skin-tones").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
        color_code: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
        color_code: {
			required: "Please Enter Colour Code",
			},
        }
})