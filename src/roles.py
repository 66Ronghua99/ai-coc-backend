from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Tuple
import random

class Role(BaseModel):
    # Basic attributes
    is_player: bool
    name: str
    STR: int = Field(description="Strength attribute")
    CON: int = Field(description="Constitution attribute")
    SIZ: int = Field(description="Size attribute")
    DEX: int = Field(description="Dexterity attribute")
    APP: int = Field(description="Appearance attribute")
    INT: int = Field(description="Intelligence attribute")
    POW: int = Field(description="Power attribute")
    EDU: int = Field(description="Education attribute")
    MOV: int = Field(description="Movement attribute")
    
    # Derived attributes
    HP: int = Field(default=0, description="Hit Points")
    MP: int = Field(default=0, description="Magic Points")
    SAN: int = Field(default=99, description="Sanity Points")
    LUCK: int = Field(default=0, description="Luck Points")
    
    # Current status
    current_hp: int = Field(default=0, description="Current Hit Points")
    current_mp: int = Field(default=0, description="Current Magic Points")
    current_san: int = Field(default=99, description="Current Sanity Points")
    current_luck: int = Field(default=0, description="Current Luck Points")
    
    # Combat attributes
    damage_bonus: str = Field(default="0", description="Damage Bonus")
    build: int = Field(default=0, description="Build value")
    
    # Skills and occupation
    skills: Dict[str, int] = Field(default_factory=dict, description="Skill name -> value")
    occupation: str
    credit_rating: int = Field(default=0, description="Credit Rating")
    
    def model_post_init(self, __pydantic_extra__: dict | None = None) -> None:
        """Initialize derived attributes after model creation."""
        # Calculate derived attributes
        self.HP = (self.CON + self.SIZ) // 10
        self.MP = self.POW // 5
        self.current_hp = self.HP
        self.current_mp = self.MP
        self.current_san = self.SAN
        self.LUCK = roll_dice(3, 6) * 5
        self.current_luck = self.LUCK
        
        # Calculate combat attributes
        self._calculate_combat_attributes()
        
    def _calculate_combat_attributes(self):
        """Calculate damage bonus and build based on STR+SIZ."""
        total = self.STR + self.SIZ
        if total <= 64:
            self.damage_bonus = "-2"
            self.build = -2
        elif total <= 84:
            self.damage_bonus = "-1"
            self.build = -1
        elif total <= 124:
            self.damage_bonus = "0"
            self.build = 0
        elif total <= 164:
            self.damage_bonus = "+1D4"
            self.build = 1
        elif total <= 204:
            self.damage_bonus = "+1D6"
            self.build = 2
        else:
            self.damage_bonus = "+2D6"
            self.build = 3
            
    def take_damage(self, damage: int, damage_type: str = "temporary") -> bool:
        """Apply damage to the player. Returns True if player is still conscious."""
        self.current_hp -= damage
        if damage_type == "permanent":
            self.HP -= damage
        return self.current_hp > 0
        
    def take_sanity_damage(self, damage: int, damage_type: str = "temporary") -> bool:
        """Apply sanity damage to the player. Returns True if player hasn't gone insane."""
        self.current_san -= damage
        if damage_type == "permanent":
            self.SAN -= damage
        return self.current_san > 0
        
    def skill_check(self, skill_name: str, difficulty: str = "normal") -> bool:
        """Perform a skill check. Returns True if successful."""
        if skill_name not in self.skills:
            return False
            
        skill_value = self.skills[skill_name]
        if difficulty == "hard":
            skill_value = skill_value // 2
        elif difficulty == "extreme":
            skill_value = skill_value // 5
            
        roll = roll_dice(1, 100)
        if roll <= skill_value:
            return True
        else:
            return False
        
    def get_skill_value(self, skill_name: str) -> int:
        """Get the current value of a skill."""
        return self.skills.get(skill_name, 0)
        
    def improve_skill(self, skill_name: str, amount: int = 1):
        """Improve a skill by the given amount."""
        if skill_name in self.skills:
            self.skills[skill_name] += amount
            
    def attack(self, weapon: str, difficulty: str = "normal") -> Tuple[bool, int]:
        """
        Perform an attack with a weapon.
        Returns (success, damage) tuple.
        """
        # Get the appropriate combat skill
        combat_skill = "格斗" if weapon in ["拳头", "踢击"] else weapon
        
        # Check if the attack hits
        success = self.skill_check(combat_skill, difficulty)
        if not success:
            return False, 0
            
        # Calculate base damage
        if weapon == "拳头":
            damage = 1
        elif weapon == "踢击":
            damage = 1
        else:
            # For weapons, damage should be defined in a weapon database
            # This is a placeholder
            damage = 1
            
        # Add damage bonus
        if self.damage_bonus.startswith("+"):
            dice_num = int(self.damage_bonus[1])
            faces = int(self.damage_bonus.split("D")[1])
            damage += roll_dice(dice_num, faces)
            
        return True, damage
        
    def dodge(self) -> bool:
        """Attempt to dodge an attack."""
        return True
        
    def fight_back(self, weapon: str, difficulty: str = "normal") -> Tuple[bool, int]:
        """
        Fight back against an attacker.
        Returns (success, damage) tuple.
        """
        return self.attack(weapon, difficulty)
        
    def get_combat_order(self) -> int:
        """Get combat order based on DEX."""
        return self.DEX
        
    def is_conscious(self) -> bool:
        """Check if the player is conscious."""
        return self.current_hp > 0
        
    def is_sane(self) -> bool:
        """Check if the player is sane."""
        return self.current_san > 0
        
    def get_status(self) -> Dict:
        """Get current status of the player."""
        return {
            "name": self.name,
            "hp": f"{self.current_hp}/{self.HP}",
            "mp": f"{self.current_mp}/{self.MP}",
            "san": f"{self.current_san}/{self.SAN}",
            "luck": self.current_luck,
            "conscious": self.is_conscious(),
            "sane": self.is_sane()
        }

class PlayerManager:
    def __init__(self):
        self.players: Dict[str, Role] = {}
        
    def add_player(self, role: Role):
        """Add a new player to the game."""
        self.players[role.name] = role
        
    def get_player(self, name: str) -> Optional[Role]:
        """Get a player by name."""
        return self.players.get(name)
        
    def remove_player(self, name: str):
        """Remove a player from the game."""
        if name in self.players:
            del self.players[name]
            
    def get_all_players(self) -> List[Role]:
        """Get all players in the game."""
        return list(self.players.values())


class NPCManager:
    def __init__(self):
        self.npcs: Dict[str, Role] = {}
        
    def add_npc(self, npc: Role):
        """Add a new NPC to the game."""
        self.npcs[npc.name] = npc

    def get_npc(self, name: str) -> Optional[Role]:
        """Get an NPC by name."""
        return self.npcs.get(name)

def roll_dice(dice_num: int, faces: int) -> int:
    """Roll a dice and return the result."""
    result = 0
    for _ in range(dice_num):
        result += random.randint(1, faces)
    return result