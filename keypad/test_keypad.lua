keypad = {}
keypad['buffer'] = ''
function backup(args)
    path = args.path
    path = path:gsub('%"', '')
    gre.set_value("keypad_backup", path .. '.text')
end
function number_single_input_keypad(args)
    local key = args.key
    local path = gre.get_value('keypad_target_path')
    path = path:gsub('%"', '')
    local range = gre.get_value('keypad_input_limit')
    gre.set_value("Input_layer.input_group.range.text", "0 - " .. range)
    if key == 'enter' then
        if keypad['buffer'] == "" then
            gre.set_value(path .. ".text", 0)
            return
        end
        gre.set_value(path .. ".text", tostring(tonumber(keypad['buffer'])))
        keypad['buffer'] = ''
        return
    end
    if key == 'delete' then
        keypad['buffer'] = keypad['buffer']:sub(1, -2)
        gre.set_value("keypad_input_buffer", keypad['buffer'] .. "_")
        return
    end
    if key == 'cancel' then
        keypad['buffer'] = ''
        return
    end
    if tonumber(keypad['buffer'] .. key) > range then
    else
        keypad['buffer'] = keypad['buffer'] .. key
    end
    gre.set_value("keypad_input_buffer", keypad['buffer'] .. "_")
end
