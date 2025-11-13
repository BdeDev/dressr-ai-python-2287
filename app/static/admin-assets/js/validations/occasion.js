$("#add-occasions").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
        }
	});  


$("#edit-occasions").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
        }
})  