from .roles import Role, PlayerManager, NPCManager, roll_dice
from typing import Dict, Any, List, Optional, Tuple
import random

# Import VectorManager for vector search operations
from .vector_manager import VectorManager

# Initialize global player manager
player_manager = PlayerManager()
npc_manager = NPCManager()

# Initialize vector manager for rule lookups
vector_manager = VectorManager()

def function_calling(function_name: str, parameters: Dict[str, Any]) -> Any:
    """
    Call a function with the given name and parameters.
    """
    # Vector search functions
    if function_name in ["search_all_rules", "get_available_rule_documents",  "retrieve_coc_rules_skills", "retrieve_coc_rules_sanity", "retrieve_coc_mythos_creatures_gods", "retrieve_coc_rules_keeper_guide", "retrieve_coc_rules_game_system", "retrieve_coc_rules_chase", "retrieve_coc_rules_combat", "retrieve_coc_rules_alien_technology", "retrieve_coc_rules_investigator_creation" ]:
        return vector_manager.function_calling(function_name, parameters)
        
    elif function_name == "roll_dice":
        return roll_dice(parameters["dice_num"], parameters["faces"])
        
    elif function_name == "create_role":
        try:
            role = Role(
                name=parameters["name"],
                STR=parameters["STR"],
                CON=parameters["CON"],
                SIZ=parameters["SIZ"],
                DEX=parameters["DEX"],
                APP=parameters["APP"],
                INT=parameters["INT"],
                POW=parameters["POW"],
                EDU=parameters["EDU"],
                MOV=parameters["MOV"],
                occupation=parameters["occupation"],
                skills=parameters.get("skills", {}),
                credit_rating=0,  # Will be set based on occupation
                # background="",
                # important_person="",
                # meaningful_location="",
                # treasured_possession="",
                # trait="",
                is_player=parameters.get("is_player")
            )
            if role.is_player: 
                player_manager.add_player(role)
            else:
                npc_manager.add_npc(role)
        except Exception as e:
            raise ValueError(f"Create_role error: {e}")
        return role.get_status()
        
    elif function_name == "perform_skill_check":
        player = player_manager.get_player(parameters["role_name"])
        if not player:
            raise ValueError(f"Role {parameters['role_name']} not found")
            
        difficulty = parameters.get("difficulty", "normal")
        allow_pushed = parameters.get("allow_pushed", False)
        
        # Perform the skill check
        success = player.skill_check(parameters["skill_name"], difficulty)
        
        # If failed and pushed roll is allowed, try again
        if not success and allow_pushed:
            success = player.skill_check(parameters["skill_name"], difficulty)
            
        return {
            "success": success,
            "skill_name": parameters["skill_name"],
            "difficulty": difficulty,
            "pushed": allow_pushed and not success
        }
        
    elif function_name == "apply_damage":
        player = player_manager.get_player(parameters["role_name"])
        if not player:
            raise ValueError(f"Role {parameters['role_name']} not found")
            
        damage = parameters["damage"]
        damage_type = parameters.get("damage_type", "normal")
        
        # Apply damage based on type
        if damage_type == "major":
            damage *= 2
            
        still_conscious = player.take_damage(damage)
        return {
            "damage_applied": damage,
            "current_hp": player.current_hp,
            "conscious": still_conscious
        }
        
    elif function_name == "apply_sanity_damage":
        player = player_manager.get_player(parameters["role_name"])
        if not player:
            raise ValueError(f"Role {parameters['role_name']} not found")
            
        damage = parameters["damage"]
        damage_type = parameters.get("damage_type", "temporary")
        
        still_sane = player.take_sanity_damage(damage, damage_type)
        return {
            "sanity_loss": damage,
            "current_san": player.current_san,
            "sane": still_sane
        }
        
    elif function_name == "perform_attack":
        if parameters["attacker_name"] in player_manager.players:
            attacker = player_manager.get_player(parameters["attacker_name"])
            target = player_manager.get_player(parameters["target_name"])
        else:
            attacker = npc_manager.get_npc(parameters["attacker_name"])
            target = npc_manager.get_npc(parameters["target_name"])

        if not attacker:
            raise ValueError(f"Attacker not found: {parameters['attacker_name']}")
        if not target:
            raise ValueError(f"Target not found: {parameters['target_name']}")
            
        weapon = parameters.get("weapon", "")
        difficulty = parameters.get("difficulty", "normal")
        
        success, damage = attacker.attack(weapon, target, difficulty)
        if success:
            target.take_damage(damage)
            
        return {
            "success": success,
            "damage": damage if success else 0,
            "target_hp": target.current_hp,
            "target_conscious": target.is_conscious()
        }
        
    elif function_name == "attempt_dodge":
        if parameters["role_name"] in player_manager.players:
            player = player_manager.get_player(parameters["role_name"])
        else:
            player = npc_manager.get_npc(parameters["role_name"])
        if not player:
            raise ValueError(f"Role {parameters['role_name']} not found")
            
        difficulty = parameters.get("difficulty", "normal")
        success = player.dodge()
        
        return {
            "success": success,
            "role_name": parameters["role_name"]
        }
        
    elif function_name == "fight_back":
        if parameters["defender_name"] in player_manager.players:
            defender = player_manager.get_player(parameters["defender_name"])
            attacker = npc_manager.get_npc(parameters["attacker_name"])
        else:
            defender = npc_manager.get_npc(parameters["defender_name"])
            attacker = npc_manager.get_npc(parameters["attacker_name"])
        if not defender:
            raise ValueError(f"Defender not found: {parameters['defender_name']}")
        if not attacker:
            raise ValueError(f"Attacker not found: {parameters['attacker_name']}")
            
        weapon = parameters.get("weapon", "")
        difficulty = parameters.get("difficulty")
        
        success, damage = defender.fight_back(weapon, difficulty)
        if success:
            attacker.take_damage(damage)
            
        return {
            "success": success,
            "damage": damage if success else 0,
        }
        
    elif function_name == "improve_skill":
        player = player_manager.get_player(parameters["role_name"])
        if not player:
            raise ValueError(f"Role {parameters['role_name']} not found")
            
        amount = parameters.get("amount", 1)
        player.improve_skill(parameters["skill_name"], amount)
        
        return {
            "skill_name": parameters["skill_name"],
            "new_value": player.get_skill_value(parameters["skill_name"])
        }
        
    elif function_name == "get_investigator_status":
        player = player_manager.get_player(parameters["role_name"])
        if not player:
            raise ValueError(f"Role {parameters['role_name']} not found")
            
        return player.get_status()
        
    elif function_name == "start_combat":
        participants = []
        for name in parameters["participants"]:
            player = player_manager.get_player(name)
            if not player:
                raise ValueError(f"Role {name} not found")
            participants.append(player)
            
        # Sort participants by DEX for combat order
        participants.sort(key=lambda p: p.get_combat_order(), reverse=True)
        
        return {
            "combat_id": str(random.randint(1000, 9999)),
            "order": [p.name for p in participants]
        }
        
    elif function_name == "end_combat":
        # Currently just returns success, could add combat summary in the future
        return {
            "combat_id": parameters["combat_id"],
            "status": "ended"
        }
        
    elif function_name == "check_madness":
        player = player_manager.get_player(parameters["role_name"])
        if not player:
            raise ValueError(f"Role {parameters['role_name']} not found")
            
        sanity_loss = parameters["sanity_loss"]
        current_san = player.current_san
        
        # Determine madness type based on sanity loss
        if sanity_loss >= 5:
            if current_san <= 0:
                madness_type = "permanent"
            elif current_san <= 5:
                madness_type = "indefinite"
            else:
                madness_type = "temporary"
        else:
            madness_type = "none"
            
        return {
            "role_name": parameters["role_name"],
            "current_san": current_san,
            "madness_type": madness_type,
            "sane": player.is_sane()
        }
        
    else:
        raise ValueError(f"Function {function_name} not found")