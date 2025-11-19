$("#add-body-types").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
        description: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
        description: {
			required: "Please Enter description",
			},
        }
	});  


$("#edit-body-types").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
        description: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Title",
			},
        description: {
			required: "Please Enter description",
			},
        }
})