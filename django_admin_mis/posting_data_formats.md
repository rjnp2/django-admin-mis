# Single Data

- {field_name} : {submitted_data}

# Inline Data

- {inline_name}-__prefix__-{field_name}:{submitted_data}
- {inline_name}-TOTAL_FORMS: {extra} or 4
- {inline_name}-INITIAL_FORMS: 0
- {inline_name}-MIN_NUM_FORMS: {min_num} or 1
- {inline_name}-MAX_NUM_FORMS: {max_num} or 1000

# Nested Inline Data

- {inline_name[0]}-__prefix__-{inline_name[1]}-__prefix__-{field_name}:{submitted_data}
- {inline_name[0]}-__prefix__-{inline_name[1]}-TOTAL_FORMS: {extra} or 4
- {inline_name[0]}-__prefix__-{inline_name[1]}-INITIAL_FORMS: 0
- {inline_name[0]}-__prefix__-{inline_name[1]}-MIN_NUM_FORMS: {min_num} or 1
- {inline_name[0]}-__prefix__-{inline_name[1]}-MAX_NUM_FORMS: {max_num} or 1000
