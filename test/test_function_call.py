import openai
from dotenv import load_dotenv
functions = [
        {
        "type": "function",
        "function": {
            "name": "roll_dice",
            "description": "Roll dice for skill checks, damage, or other random events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dice_num": {
                        "type": "integer",
                        "description": "Number of dice to roll"
                    },
                    "faces": {
                        "type": "integer",
                        "description": "Number of faces on each die"
                    },
                    "bonus": {
                        "type": "integer",
                        "description": "Optional bonus to add to the roll"
                    }
                },
                "required": ["dice_num", "faces"],
                "additionalProperties": False
            }
        },
    }, 
    {
        "type": "function",
        "function": {
            "name": "create_role",
            "description": "Create a new role with specified attributes.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the role"
                },
                "STR": {
                    "type": "integer",
                    "description": "Strength attribute (3D6*5)"
                },
                "CON": {
                    "type": "integer",
                    "description": "Constitution attribute (3D6*5)"
                },
                "SIZ": {
                    "type": "integer",
                    "description": "Size attribute (2D6+6)*5"
                },
                "DEX": {
                    "type": "integer",
                    "description": "Dexterity attribute (3D6*5)"
                },
                "APP": {
                    "type": "integer",
                    "description": "Appearance attribute (3D6*5)"
                },
                "INT": {
                    "type": "integer",
                    "description": "Intelligence attribute (2D6+6)*5"
                },
                "POW": {
                    "type": "integer",
                    "description": "Power attribute (3D6*5)"
                },
                "EDU": {
                    "type": "integer",
                    "description": "Education attribute (2D6+6)*5"
                },
                "occupation": {
                    "type": "string",
                    "description": "Role's occupation"
                },
                "skills": {
                    "type": "object",
                    "description": "Initial skills and their values",
                    "additionalProperties": {
                        "type": "integer",
                        "description": "Skill value"
                    }
                }
            },
            "required": ["name", "STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "EDU", "occupation"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "perform_skill_check",
        "description": "Perform a skill check for a role.",
        "parameters": {
            "type": "object",
            "properties": {
                "role_name": {
                    "type": "string",
                    "description": "Name of the role"
                },
                "skill_name": {
                    "type": "string",
                    "description": "Name of the skill to check"
                },
                "difficulty": {
                    "type": "string",
                    "description": "Difficulty level (easy/normal/hard/extreme)",
                    "enum": ["easy", "normal", "hard", "extreme"]
                },
                "allow_pushed": {
                    "type": "boolean",
                    "description": "Whether to allow pushed roll on failure"
                }
            },
            "required": ["role_name", "skill_name", "difficulty", "allow_pushed"],
            "additionalProperties": False
            },
            "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "apply_damage",
        "description": "Apply physical damage to a role.",
        "parameters": {
            "type": "object",
            "properties": {
                "role_name": {
                    "type": "string",
                    "description": "Name of the role"
                },
                "damage": {
                    "type": "integer",
                    "description": "Amount of damage to apply"
                },
                "damage_type": {
                    "type": "string",
                    "description": "Type of damage (normal/major)",
                    "enum": ["normal", "major"]
                }
            },
            "required": ["role_name", "damage", "damage_type"],
            "additionalProperties": False
            },
            "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "apply_sanity_damage",
        "description": "Apply sanity damage to a role.",
        "parameters": {
            "type": "object",
            "properties": {
                "role_name": {
                    "type": "string",
                    "description": "Name of the role"
                },
                "damage": {
                    "type": "integer",
                    "description": "Amount of sanity damage to apply"
                },
                "damage_type": {
                    "type": "string",
                    "description": "Type of sanity damage (temporary/indefinite/permanent)",
                    "enum": ["temporary", "indefinite", "permanent"]
                }
            },
            "required": ["role_name", "damage", "damage_type"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "perform_attack",
        "description": "Perform an attack with a weapon.",
        "parameters": {
            "type": "object",
            "properties": {
                "attacker_name": {
                    "type": "string",
                    "description": "Name of the attacking role"
                },
                "target_name": {
                    "type": "string",
                    "description": "Name of the target role"
                },
                "weapon": {
                    "type": ["string", "null"],
                    "description": "Weapon used for the attack"
                },
                "difficulty": {
                    "type": "string",
                    "description": "Difficulty level of the attack",
                    "enum": ["normal", "hard", "extreme"]
                }
            },
            "required": ["attacker_name", "target_name", "weapon", "difficulty"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "attempt_dodge",
        "description": "Attempt to dodge an attack.",
        "parameters": {
            "type": "object",
            "properties": {
                "role_name": {
                    "type": "string",
                    "description": "Name of the role attempting to dodge"
                },
                "difficulty": {
                    "type": "string",
                    "description": "Difficulty level of the dodge",
                    "enum": ["easy", "normal", "hard", "extreme"]
                }
            },
            "required": ["role_name", "difficulty"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "fight_back",
        "description": "Fight back against an attacker during combat.",
        "parameters": {
            "type": "object",
            "properties": {
                "defender_name": {
                    "type": "string",
                    "description": "Name of the role fighting back"
                },
                "attacker_name": {
                    "type": "string",
                    "description": "Name of the role being fought back against"
                },
                "weapon": {
                    "type": ["string", "null"],
                    "description": "Weapon used for the counter-attack"
                },
                "difficulty": {
                    "type": "string",
                    "description": "Difficulty level of the counter-attack",
                    "enum": ["easy", "normal", "hard", "extreme"]
                },
            },
            "required": ["defender_name", "attacker_name", "difficulty", "weapon"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "improve_skill",
        "description": "Improve a skill after successful use.",
        "parameters": {
            "type": "object",
            "properties": {
                "role_name": {
                    "type": "string",
                    "description": "Name of the role"
                },
                "skill_name": {
                    "type": "string",
                    "description": "Name of the skill to improve"
                },
                "amount": {
                    "type": "integer",
                    "description": "Amount to improve the skill by"
                }
            },
            "required": ["role_name", "skill_name", "amount"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "get_investigator_status",
        "description": "Get current status of a role.",
        "parameters": {
            "type": "object",
            "properties": {
                "role_name": {
                    "type": "string",
                    "description": "Name of the role"
                }
            },
            "required": ["role_name"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "start_combat",
        "description": "Start a combat encounter between roles.",
        "parameters": {
            "type": "object",
            "properties": {
                "participants": {
                    "type": "array",
                    "description": "List of role names participating in combat",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["participants"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "end_combat",
        "description": "End a combat encounter.",
        "parameters": {
            "type": "object",
            "properties": {
                "combat_id": {
                    "type": "string",
                    "description": "ID of the combat to end"
                }
            },
            "required": ["combat_id"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
    {
        "type": "function",
        "function": {
        "name": "check_madness",
        "description": "Check if a role has gone mad.",
        "parameters": {
            "type": "object",
            "properties": {
                "role_name": {
                    "type": "string",
                    "description": "Name of the role"
                },
                "sanity_loss": {
                    "type": "integer",
                    "description": "Amount of sanity lost in the current incident"
                }
            },
            "required": ["role_name", "sanity_loss"],
            "additionalProperties": False
        },
        "strict": True
        },
    },
]



load_dotenv()

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Call the roll_dice function to roll a 20-sided die."}],
    tools=functions
)

print(response.choices[0].message.tool_calls)