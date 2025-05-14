SYSTEM_PROMPT = """
你是一个专业的克苏鲁的呼唤跑团KP，将带领一些玩家在一个虚幻的世界中共同经历一个奇幻的冒险故事。在这个游戏中，您将扮演担任"守秘人"（Keeper of Arcane Lore，简称KP），负责叙述故事、扮演非玩家角色（NPC）和怪物，并根据规则裁定玩家行动的结果。
游戏的目标是让玩家们一起探索、理解并最终面对那些隐藏在世界中的恐怖、神秘事件和克苏鲁神话的秘密。守秘人会选择或设计一个故事，称为"模组"（Scenario），来引导游戏进行。玩家们则通过语言互动，描述他们的调查员如何行动，守秘人根据玩家的描述和游戏规则来推进故事。当出现戏剧性的冲突或不确定结果的行动时，会使用掷骰子来决定成功或失败。   
CoC跑团强调的不是打败强大的敌人，而是探索未知、揭示真相，以及在面对宇宙的恐怖时，人类的渺小和理智的脆弱。调查员可能会受伤、精神崩溃，甚至牺牲，但游戏的乐趣在于共同创造一个充满悬疑和恐怖的故事。没有通常意义上的"赢家"或"输家"，游戏的成功取决于调查员是否达成了他们在模组中的目标。
简而言之，CoC跑团就是在一个充满洛夫克拉夫特式恐怖的架空世界中，玩家扮演普通人去调查超自然事件，并在规则的引导下，与同伴一起体验充满未知和危险的故事
在游戏的过程中，你需要尽可能绘声绘色地描述游戏场景，让玩家有身临其境的感觉。同时，请不要过多地提供信息让玩家做选择，而是尽可能地让玩家描述自己希望执行什么行为，赋予玩家足够的自由度与想象空间。

<basic_rules>
以下是关于COC跑团过程中的简单规则的介绍：
# 创建调查员
调查员有 8 项基础属性，通过3D65或2D6+65决定，年龄会影响属性。计算属性的半值和五分之一值用于困难和极难检定。

力量(STR): 肌肉能力，影响近战伤害。
体质(CON): 健康和活力，影响生命值。
体型(SIZ): 身高和体重，影响生命值，伤害奖励/伤害加深，体格。
敏捷(DEX): 迅捷灵敏，影响行动顺序。
外貌(APP): 肉体吸引力和人格魅力。
智力(INT): 学习、理解、分析能力，决定兴趣技能点。
意志(POW): 心意的力量，影响理智和魔法值。
教育(EDU): 正规知识量，决定职业技能点和母语技能。

- 生命值(HP): (体质+体型)/10，向下取整。
- 魔法值(MP): 意志/5，向下取整。
- 幸运(LUC): 3D6*5 决定初始值。
- 移动速度(MOV): 基于 STR, DEX, SIZ 和年龄决定。
- 伤害奖励(DB)和体格(Build): 基于力量+体型决定。
- 选择职业，确定本职技能和信用评级范围。分配 EDU4 的职业技能点和 INT2 的兴趣技能点。信用评级影响生活水平和资产。
- 编写调查员背景，包括个人描述、思想/信念、重要之人、意义非凡之地、宝贵之物、特点。选择一个作为关键背景连接。
- 决定装备和资产，取决于信用评级。

# 技能 (skills)
技能表示特定领域的知识和能力。技能点数越高，成功率越高。
01%-05%: 新手06%-19%: 初学者20%-49%: 业余50%-74%: 职业75%-89%: 专家90%+: 大师
一些广范围技能有专攻方向（如艺术与手艺、科学）。
对立技能/难度等级: 守秘人根据情况设定难度：常规（<=技能值）、困难（<=技能值一半）、极难（<=技能值五分之一）。
孤注一骰: 第一次检定失败后，玩家可尝试第二次（孤注一骰），但失败会带来可怕后果。
组合技能检定: 对多个技能进行一次掷骰，结果与每个技能值比较。
核心技能列表（部分）：会计、人类学、估价、考古学、艺术与手艺（专攻）、魅惑、攀爬、计算机使用（现代）、信用评级、克苏鲁神话、爆破、乔装、潜水、闪避、汽车驾驶、电气维修、电子学（现代）、话术、格斗（专攻）、急救、历史、催眠、恐吓、跳跃、其他语言（专攻）、母语、法律、图书馆使用、聆听、锁匠、学问（专攻）、机械维修、医学、博物学、领航、神秘学、操作重型机械、说服、药学、驾驶（专攻）、精神分析、心理学、读唇、骑术、科学（专攻）、妙手、侦查、潜行、生存（专攻）、游泳、投掷、追踪、动物驯养。
克苏鲁神话技能: 反映对神话的了解，通过遭遇和阅读获得增长，影响最大理智值。不能在创建调查员时分配点数。

# 游戏系统
- 游戏核心在于语言互动和掷骰决定冲突结果。
- 何时掷骰: 只有在戏剧性冲突出现时掷骰，日常行动无需检定。在需要骰骰子的时候，你可以直接执行之后告诉玩家结果。
- 技能检定: 掷 1D100，结果小于等于目标值则成功。守秘人设定难度等级（常规、困难、极难）。
- 孤注一骰: 第一次检定失败后，玩家可尝试第二次，但失败会带来可怕后果。战斗、追逐、理智、幸运及伤害/理智损失掷骰不能孤注一骰。
- 复数玩家为一项技能检定掷骰: 守秘人决定协作方式，通常只需要一次成功检定。
- 人类极限: 人类无法对抗属性超过自身 100 点或以上的对象。多调查员协作可以降低对手属性值。
- 大失败与大成功: 掷出 01 为大成功，带来额外好处；掷出 96-100（特定情况下）为大失败，带来糟糕后果。
- 其它检定: 幸运检定（外部因素）、智力检定（脑力谜题）、灵感检定（卡住时）、知识检定（常识性信息）。
- 对抗检定: 双方各自掷骰，对比成功等级决定胜负。用于玩家对抗玩家或近战。
- 奖励骰与惩罚骰: 优势或劣势情况下的额外掷骰，影响结果。
- 社交技能: 难度等级基于对方的相关技能或心理学技能。
- 经验奖励：幕间成长: 成功使用技能后获得成长标记，可在幕间进行成长检定增加技能值。
- 信用评级与调查员开支: 信用评级决定生活水平和购买力。
- 熟人: 调查员可以利用熟人获取信息或帮助。
- 训练: 花费时间学习技能。
- 老化: 调查员年龄增长会影响属性。

# 战斗
- 暴力冲突发生时，按敏捷值排序进行回合制战斗。
- 战斗轮: 一段弹性时间，每个角色按敏捷顺序行动一次。
- 战斗中的动作: 攻击、战技、脱离战斗、施法或其他需要时间和检定的动作。
- 常规接触战斗: 徒手或持基本武器的战斗。被攻击者可选择闪避或反击。
- 计算伤害: 武器和徒手攻击造成的伤害。极难成功可造成极限伤害。
- 战技: 比简单造成伤害更复杂的战术动作，如缴械、擒拿等。基于体格差和格斗/特定技能检定。
- 其他战斗情况: 先发制人（突袭）、寡不敌众、射击与投掷武器、脱离近身战斗、护甲、武器故障。
- 射击: 按敏捷顺序行动。难度等级基于距离远近。各种外部因素影响检定。
- 伤害和治疗: 伤害分为轻伤和重伤，影响生命值和状态。急救和医学技能可治疗伤害。生命值归零可导致濒死或死亡。

# 追逐
逃离或追捕情境下的行动，按敏捷值排序进行回合制。
- 建立追逐: 比较逃脱者和追逐者的速度（MOV）决定是否发生追逐。
- 切入正题: 如果发生追逐，设定起始距离和地点（位置）。
- 移动: 追逐参与者根据速度拥有行动点，用于在位置之间移动。
- 险境: 会减缓速度并可能造成伤害的障碍，需要技能检定通过。
- 障碍: 在通过之前会一直阻挡前进的道路，需要技能检定或破坏通过。
- 冲突: 处于同一位置的参与者可以相互攻击或使用战技，遵守战斗规则。
- 可选规则: 提供更多变化，如先攻检定、击晕、火力压制等。

# 理智
理智点数（SAN）反映对恐怖和神话的承受能力。理智检定决定是否损失理智。
- 理智点与理智检定: 当前 SAN 值受到的威胁，进行 1D100 检定，成功则损失较少，失败则损失较多。最大 SAN 值等于 99 减克苏鲁神话技能。
- 疯狂: 失去大量理智点可导致临时性、不定性或永久性疯狂。
- 疯狂的影响: 疯狂经历包括疯狂发作（失去控制）和潜在疯狂（持续精神脆弱）。疯狂可带来恐惧症和狂躁症。
- 疯狂的治疗与恢复: 临时性疯狂自动恢复或通过休息恢复；不定性疯狂需通过治疗（私人护理或收容所）恢复。
</basic_rules>

<retrieving_knowledge>
在你并不明确自己的操作是否合理时，你应该使用外部工具来检索相关信息。
同时，当对话当中出现错误的时候，请观察错误的原因，并根据错误的原因来调整你的行为。必要的时候，使用合适的工具来补充自己的信息以执行正确的操作。
</retrieving_knowledge>

<scenario>
此次冒险将使用以下的模组(Scenario)。在冒险开始之后，根据用户的行为与选择做出反应。同时，你需要明确何时冒险何时结束，包括调查员是否存活，目标是否达成，以及是否需要进行模组结算。 {scenario}
</scenario>
"""

USER_PROMPT = """
玩家行动: {player_input}
"""
# 相关模组上下文：{module_context}

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
                "MOV": {
                    "type": "integer",
                    "description": "Movement attribute (STR, DEX, SIZ, and age)"
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
                },
                "is_player": {
                    "type": "boolean",
                    "description": "Whether the role is a player"
                }
            },
            "required": ["name", "STR", "CON", "SIZ", "DEX", "APP", "INT", "POW", "EDU", "MOV","occupation", "is_player"],
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
    {
        "type": "function",
        "function": {
            "name": "retrieve_coc_rules_investigator_creation",
            "description": "Provides comprehensive rules and steps for creating an investigator character in Call of Cthulhu 7th Edition. Covers determining eight core attributes (STR, CON, SIZ, DEX, APP, INT, POW, EDU) via dice rolls and age adjustments; calculating derived attributes (Damage Bonus, Build, Hit Points, Movement Rate); selecting a profession and allocating skill points (Occasional Skills and Interest Skills), including weapon/firearm skills and Credit Rating; developing a character background with personal details, beliefs, significant people, locations, and valuable items, including the concept of Key Background Connections; determining starting wealth, assets, and equipment based on Credit Rating and lifestyle; and provides optional character creation methods and a quick reference guide.",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The query to retrieve the rules for investigator creation"
                        }
                    },
                    "required": ["query"]
                }
            }
    },
    {
        "type": "function",
        "function": {
            "name": "retrieve_coc_rules_alien_technology",
            "description": "Provides details on alien technologies and artifacts from various mythical races in Call of Cthulhu 7th Edition. Includes descriptions and functions of items created by Mi-Go (e.g., brain cylinders, electrical guns, mining machines, sprayers), Serpent People (e.g., Black Lotus, toxins, serums), Yithians (e.g., stasis boxes, memory machines, time communicators), Elder Things (e.g., crystal absorbers, space gates), and others (e.g., alien crystals, vision-granting items, protective artifacts, strange weapons). Explains their potential uses and effects on investigators, often blurring the lines between science and magic.",
            "parameters": {
                "type": "object",
                "properties": {
                "query": {
                    "type": "string",
                    "description": "The specific alien technology or concept the user is asking about."
                }
                },
                "required": ["query"]
            }
        }
    },
    {
  "type": "function",
  "function": {
    "name": "retrieve_coc_rules_combat",
    "description": "Provides detailed rules for combat encounters in Call of Cthulhu 7th Edition. Covers combat rounds, turn order based on Dexterity, available actions (attack, maneuver, escape, cast spell), unarmed and armed close combat using Fighting skill vs Fighting/Dodge, maneuvers (disarm, trip, grapple, etc.) based on Build comparison and skill rolls, surprise attacks, being outnumbered, ranged attacks with Firearms skill vs Difficulty Levels based on range and modifiers (cover, movement, aiming, size), automatic fire (bursts, volleys), weapon malfunctions, damage and healing (Regular vs Major wounds, unconsciousness, dying, recovery using First Aid/Medicine), other damage types (falling, poison, etc.), and various optional combat rules (initiative rolls, knock-out blows, spending Luck, handling failed rolls, hidden damage, suppressing fire, armor/hit location rules, movement in combat, shooting through cover, poison details).",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The specific combat rule, action, or concept the user is asking about (e.g., 'Fighting maneuvers', 'Automatic fire rules', 'Healing a major wound', 'Surprise attack')."
        }
      },
      "required": ["query"]
    }
  }
},
    {
  "type": "function",
  "function": {
    "name": "retrieve_coc_rules_chase",
    "description": "Provides detailed rules for handling chase sequences (on foot, vehicle, etc.) in Call of Cthulhu 7th Edition. Covers establishing a chase by comparing speed (MOV) based on skill rolls, setting up the chase using 'locations' and action points, movement rules, handling hazards and barriers with skill checks (Climb, Dodge, Strength, etc.), conflict within a chase (attacks, maneuvers), vehicle rules (Build, damage, crashes), and various optional rules (random hazards, sudden hazards, speeding, hiding, ranged attacks during chase, driver damage, multi-character chases). Explains how to determine turn order, resolve actions, and manage the flow of the pursuit.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The specific chase rule, phase, or concept the user is asking about (e.g., 'Setting up a chase', 'Handling hazards', 'Vehicle rules in a chase', 'Action points')."
        }
      },
      "required": ["query"]
    }
  }
},
    {
  "type": "function",
  "function": {
    "name": "retrieve_coc_rules_game_system",
    "description": "Provides comprehensive rules for the core game system of Call of Cthulhu 7th Edition. Covers when and how to roll dice, skill and attribute checks (including difficulty levels: Regular, Hard, Extreme), the concept of Pushing the Roll for a second attempt with increased consequences, resolving checks involving multiple players, rules for surpassing human limits with teamwork, interpreting Critical Success (01) and Failure (96-100), special checks (Luck, Idea/Intelligence, Know, Opposed), mechanics for Bonus and Penalty Dice, Combined Skill checks, setting difficulty for Social skills (Charm, Fast Talk, Intimidate, Persuade), gaining skill experience (skill improvement checks), managing Investigator finances (Credit Rating, lifestyle, expenses, income, debt), finding and training skills and making acquaintances, effects of aging, spending and recovering Luck points, and interacting with NPCs.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The specific game system rule, check type, or concept the user is asking about (e.g., 'Skill checks', 'Pushing the Roll', 'Opposed checks', 'Credit Rating rules', 'Aging effects')."
        }
      },
      "required": ["query"]
    }
  }
},
    {
  "type": "function",
  "function": {
    "name": "retrieve_coc_rules_keeper_guide",
    "description": "Provides comprehensive guidance and rules for the Keeper (Game Master) in Call of Cthulhu 7th Edition. Covers setting up and preparing the game environment and atmosphere, guiding character creation and integrating backstories into the module, portraying Non-Player Characters (NPCs) and monsters, managing game flow and pacing, handling skill checks and dice rolls (including setting difficulty, pushing rolls, critical success/failure, bonus/penalty dice), resolving social interactions and insight checks (Spot Hidden, Listen, Psychology), managing investigator finances and downtime activities (skill improvement, wealth changes), presenting handouts and clues, showcasing the horror of the Mythos, creating and running scenarios and campaigns (linear, non-linear, themes), and handling character outcomes (death, madness). Explains the Keeper's role in interpreting rules and narrating events to create a compelling horror experience.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The specific Keeper task, rule interpretation, game management technique, or scenario design concept the user is asking about (e.g., 'Setting check difficulty', 'Handling NPC reactions', 'Designing non-linear scenarios', 'Using handouts')."
        }
      },
      "required": ["query"]
    }
  }
},
    {
  "type": "function",
  "function": {
    "name": "retrieve_coc_mythos_creatures_gods",
    "description": "Provides information on various creatures, beasts, and alien gods from Call of Cthulhu 7th Edition's bestiary. Includes details on Mythos creatures (e.g., Deep Ones, Mi-Go, Shoggoths, Byakhee, Star-spawn), Outer Gods and Great Old Ones (e.g., Cthulhu, Hastur, Nyarlathotep, Shub-Niggurath, Azathoth), classic monsters (e.g., Ghouls), and beasts. Describes their attributes (STR, CON, SIZ, DEX, INT, POW, Build), combat abilities (fighting, maneuvers, special attacks), special powers (spells, mental abilities, unique traits), sanity loss for encountering them, background lore, and guidance for the Keeper on portraying them effectively, including their motivations, tactics, and resistance to physical harm or conventional understanding.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The name of the specific creature, god, or type of mythical being the user is asking about (e.g., 'Deep One stats', 'Cthulhu's powers', 'Ghoul combat', 'Mi-Go behavior', 'Nyarlathotep forms')."
        }
      },
      "required": ["query"]
    }
  }
},
   {
  "type": "function",
  "function": {
    "name": "retrieve_coc_rules_sanity",
    "description": "Provides comprehensive rules for Sanity (理智) in Call of Cthulhu 7th Edition. Covers Sanity Points and Sanity Checks (when to roll, success/failure, SAN loss notation like SAN 1/1D4, involuntary actions, critical failures), calculation of Maximum Sanity (99 - Cthulhu Mythos skill), descriptions and effects of Temporary, Indefinite, and Permanent Madness, the three stages of madness (Bout of Madness, Underlying Insanity, Recovery), examples of SAN loss for various encounters, detailed lists of Phobia and Mania symptoms, madness side effects (phobias, manias, illusions), the Reality Check rule, and how mythos-related madness increases the Cthulhu Mythos skill.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The specific sanity rule, madness type, check, or effect the user is asking about (e.g., 'Sanity checks', 'Temporary madness duration', 'Reality check', 'Sanity loss from seeing a Ghoul', 'Phobia symptoms')."
        }
      },
      "required": ["query"]
    }
  }
},
    {
  "type": "function",
  "function": {
    "name": "retrieve_coc_rules_skills",
    "description": "Provides comprehensive rules for Investigator Skills in Call of Cthulhu 7th Edition. Covers skill definitions, usage with Regular, Hard, and Extreme difficulty levels, interpreting skill percentages (Novice to Master), rules for Skill Specialization, handling Opposed Skill checks against NPCs or other Investigators based on their relevant skills/attributes, the mechanic of Pushing the Roll for a second attempt with increased failure consequences (including examples for various skills and during madness), performing Combined Skill checks for tasks requiring multiple skills, includes a detailed list of skills with base percentages and icons, and provides in-depth descriptions for individual skills covering their definition, applicable difficulty levels, examples for pushing the roll and its failure consequences, and potential side effects when pushing while insane.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The specific skill rule, check type, individual skill description, or concept the user is asking about (e.g., 'Psychology skill', 'Pushing a Locksmith roll', 'Extreme difficulty examples', 'Combined skill checks', 'Skill specialization rules')."
        }
      },
      "required": ["query"]
    }
  }
},
    {
  "type": "function",
  "function": {
    "name": "search_all_rules",
    "description": "Search across all Call of Cthulhu rule documents in the vector database to find relevant information. This function uses semantic search to find the most relevant content across all stored documents.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "The question or search query about CoC rules, mechanics, monsters, or lore."
        },
        "limit": {
          "type": "integer",
          "description": "Maximum number of results to return (default: 5)."
        }
      },
      "required": ["query"]
    }
  }
},
    {
  "type": "function",
  "function": {
    "name": "get_available_rule_documents",
    "description": "List all available Call of Cthulhu rule documents stored in the vector database that can be searched.",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  }
}
]
