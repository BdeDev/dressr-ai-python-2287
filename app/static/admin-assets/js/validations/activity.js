$("#add-activity-flags").validate({
	ignore: [],
	rules: {
		name: {
			required: true,
			},
        description: {
			required: true,
			},
		},
	messages: {
		name: {
			required: "Please Enter Name",
			},
        description: {
			required: "Please Enter Description",
			},
        }
	});  


$("#edit-activity-flags").validate({
	ignore: [],
	rules: {
		name: {
			required: true,
			},
        description: {
			required: true,
			},
		},
	messages: {
		name: {
			required: "Please Enter name",
			},
        description: {
			required: "Please Enter Description",
			},
        }
})