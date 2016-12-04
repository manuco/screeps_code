
var roleHarvester = {
	
	prepare: function() {
	},
	
	
	
	/** @param {Creep} creep **/
	run: function(creep) {
		// creeps have always the same source assigned
		// once assigned they shouldn't change
		if (creep.memory.sourceId === undefined) {
			creep.memory.sourceId = creep.pos.findClosestByPath(FIND_SOURCES).id;
		}
		
		if (creep.carry.energy >= creep.carryCapacity) {
			creep.memory.state = "building";
			
		} else if (creep.carry.energy == 0) {
			creep.memory.state = "harvesting";
		} else if (creep.carry.energy < creep.carryCapacity && creep.memory.state == "idle") {
			creep.memory.state = "harvesting";
		}
		
		if (creep.memory.state == "building") {
			if (creep.memory.destId === undefined) {
				
				var dest = creep.pos.findClosestByPath(FIND_MY_CONSTRUCTION_SITES);
				
				if (dest !== null) {
					creep.memory.destId = dest.id;
				} else {
					creep.memory.state = "repairing";
				}
			} else {
				var dest = Game.getObjectById(creep.memory.destId);
			}
		}
		
		if (creep.memory.state == "building") {
			
			var result = creep.build(dest);
			
			if (result == ERR_NOT_IN_RANGE) {
				creep.moveTo(dest);
			} else if (result == ERR_INVALID_TARGET) {
				delete creep.memory.destId;
			}
		}
		
		if (creep.memory.state == "harvesting") {
			var source = Game.getObjectById(creep.memory.sourceId);
			if (creep.harvest(source) == ERR_NOT_IN_RANGE) {
				creep.moveTo(source);
			}
		}
		
		if (creep.memory.state == "idle") {
			if (creep.memory.destId === undefined) {
				var dest = creep.pos.findClosestByPath(FIND_FLAGS, {
					filter: (flag) => {
						return (flag.name == "builders");
					}
				});
				if (dest !== null) {
					creep.memory.destId = dest.id;
				}
			} else {
				var dest = Game.getObjectById(creep.memory.destId);
			}
			
			if (dest !== null) {
				creep.moveTo(dest);
			}
		}
	}
};

module.exports = roleHarvester;
