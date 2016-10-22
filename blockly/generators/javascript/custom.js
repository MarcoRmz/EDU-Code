//start token
Blockly.JavaScript['start'] = function(block) {
  // TODO: Assemble JavaScript into code variable.
  var code = 'start\n';
  return code;
};

//var declaracion
Blockly.JavaScript['var_declaracion'] = function(block) {
  var dropdown_var_type = block.getFieldValue('var_type');
  var text_var_id = block.getFieldValue('var_id');
  // TODO: Assemble JavaScript into code variable.
  var code = dropdown_var_type + ' ' + text_var_id + '\n';
  return code;
};
