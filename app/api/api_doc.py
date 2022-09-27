user_model = \
    {
        "User": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string"
                },
                "birthday": {
                    "type": "string"
                },
                "email": {
                    "type": "string"
                },
                "gender": {
                    "type": "string"
                },
                "height": {
                    "type": "number"
                },
                "weight": {
                    "type": "number"
                },
                "role": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "name": {
                    "type": "string"
                },
                "create_time": {
                    "type": "string"
                },
                "update_time": {
                    "type": "string"
                },
                "eth_account": {
                    "type": "string"
                },
                "eth_password": {
                    "type": "string"
                },
            }
        }
    }

user_list = \
    {
        "UserList": {
            "type": "array",
            "items": user_model["User"]
        }
    }

record_model = \
    {
        "Record": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string"
                },
                "angles": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "sec": {
                                "type": "number"
                            },
                            "angle": {
                                "type": "number"
                            }
                        }
                    }
                },
                "times": {
                    "type": "number"
                },
                "fails": {
                    "type": "number"
                },
                "part": {
                    "type": "string"
                },
                "pr": {
                    "type": "string"
                },
                "test_result": {
                    "type": "string"
                },
                "create_time": {
                    "type": "string"
                },
            }
        }
    }

record_list = \
    {
        "RecordList": {
            "type": "array",
            "items": record_model["Record"]
        }
    }

todo_model = \
    {
        "UserTodo": {
            "type": "object",
            "properties": {
                "target_times": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "times": {
                                "type": "number"
                            },
                            "set": {
                                "type": "number"
                            },
                            "total": {
                                "type": "number"
                            }
                        }
                    }
                },
                "target_date": {
                    "type": "string"
                },
                "complete": {
                    "type": "boolean"
                },
                "actual_times": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "left": {
                                "type": "object",
                                "properties": {
                                    "times": {
                                        "type": "number"
                                    }
                                }
                            },
                            "right": {
                                "type": "number",
                                "properties": {
                                    "times": {
                                        "type": "number"
                                    }
                                }
                            },
                        }
                    }
                },
            }
        }
    }

target_model = \
    {
        "Target": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string"
                },
                "start_date": {
                    "type": "string"
                },
                "end_date": {
                    "type": "string"
                },
                "user_todos": {
                    "type": "array",
                    "items": todo_model["UserTodo"]
                },
            }
        }
    }


user_signup = {
    "parameters": [
        {"name": "user_id", "in": "Body", "type": "string", "required": "true"},
        {"name": "password", "in": "Body", "type": "string", "required": "true"},
        {"name": "email", "in": "Body", "type": "string", "required": "true"},
        {"name": "gender", "in": "Body", "type": "number", "required": "true"},
        {"name": "role", "in": "Body", "type": "number", "required": "true"},
        {"name": "height", "in": "Body", "type": "number"},
        {"name": "weight", "in": "Body", "type": "number"},
        {"name": "birthday", "in": "Body", "type": "string", "required": "true"},
    ], "responses": {
        "200": {
            "description": "使用者註冊成功",
            "examples": {
                "message": "註冊成功"
            }
        },
        "500": {
            "description": "使用者註冊失敗",
        }
    }
}


user_login = {
    "parameters": [
        {"name": "user_id", "in": "Body", "type": "string", "required": "true"},
        {"name": "password", "in": "Body", "type": "string", "required": "true"},
    ], "responses": {
        "200": {
            "description": "使用者登入成功",
            "examples": {
                "message": "登入成功"
            }
        },
        "500": {
            "description": "使用者登入失敗",
        }
    }
}

user_search = {
    "definitions": user_list,
    "responses": {
        "200": {
            "description": "查詢所有使用者成功",
            "schema": {
                "$ref": "#/definitions/UserList"
            },
        },
        "500": {
            "description": "查詢所有使用者失敗",
        }
    }
}


user_get = {
    "definitions": user_model,
    "responses": {
        "200": {
            "description": "查詢使用者成功",
            "schema": {
                "$ref": "#/definitions/User"
            },
        },
        "500": {
            "description": "查詢使用者失敗",
        }
    }
}

record_get = {
    "definitions": record_model,
    "responses": {
        "200": {
            "description": "查詢所有測試紀錄成功",
            "schema": {
                "$ref": "#/definitions/Record"
            },
        },
        "500": {
            "description": "查詢所有測試紀錄失敗",
        }
    }
}


record_search = {
    "definitions": record_list,
    "responses": {
        "200": {
            "description": "查詢所有測試紀錄成功",
            "schema": {
                "$ref": "#/definitions/RecordList"
            },
        },
        "500": {
            "description": "查詢所有測試紀錄失敗",
        }
    }
}

target_get = {
    "definitions": target_model,
    "responses": {
        "200": {
            "description": "查詢訓練計劃表成功",
            "schema": {
                "$ref": "#/definitions/Target"
            },
        },
        "500": {
            "description": "查詢訓練計劃表失敗",
        }
    }
}
