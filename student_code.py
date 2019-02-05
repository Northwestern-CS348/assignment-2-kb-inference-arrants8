import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        
        

        
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

   
            """An asserted fact should only be removed if it is unsupported.
An asserted rule should never be removed.
Use the supports_rules and supports_facts fields to find and adjust
facts and rules that are supported by a retracted fact.
The supported_by lists in each fact/rule that it supports needs to
be adjusted accordingly.
If a supported fact/rule is no longer supported as a result of
retracting this fact (and is not asserted), it should also be removed."""

    def kb_delete(self, fact_or_rule):
        if isinstance(fact_or_rule, Fact):
            fact = self._get_fact(fact_or_rule)
            #if asserted or supported, return
            if fact.asserted or fact.supported_by:
                return
            #if not asserted and empty, delete 
            else:
                #look at each supported fact, remove fact from supported things, see if fact needs to be deleted
                for x in fact.supported_facts:
                    newfact = self._get_fact(x)
                    #remove from supported by 
                    for y in newfact.supported_by:
                        if newfact.supported_by[y][0].statement == fact.statement:
                            newfact.supported_by.remove([y][0])       
                    self.kb_delete(fact)
                    return
                for x in fact.supported_rules:
                    newrule = self._get_rule(x)
                    #remove from supported by 
                    for y in newrule.supported_by:
                        if newrule.supported_by[y][0] == rule:
                            newrule.supported_by.remove([y][0])       
                    self.kb_delete(rule)
                


        #if passed a rule 
        else:
            rule = self._get_rule(fact_or_rule)
            #if asserted or supported, return
            if rule.asserted or rule.supported_by:
                return
            #if not asserted and empty, delete 
            else:
                #look at each supported fact, remove fact from supported things, see if fact needs to be deleted
                for x in rule.supported_facts:
                    newfact = self._get_fact(x)
                    #remove from supported by 
                    for y in newfact.supported_by:
                        if newfact.supported_by[y][0].statement == fact.statement:
                            newfact.supported_by.remove([y][0])       
                    self.kb_delete(fact)
                    return
                for x in rule.supported_rules:
                    newrule = self._get_rule(x)
                    #remove from supported by 
                    for y in newrule.supported_by:
                        if newrule.supported_by[y][0] == rule:
                            newrule.supported_by.remove([y][0])       
                    self.kb_delete(rule)
                    return
         


    

    def kb_retract(self, fact1):
         fact = self._get_rule(fact1)
         if fact.asserted:
             fact.asserted = False
         self.kb_delete(fact)
         return
         
         printv("Retracting {!r}", 0, verbose, [fact])
        ####################################################
        # Student code goes here
        

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):

        newBindings = match(fact.statement, rule.lhs[0])


        ## if there is a match with the fact and 1st element of LHS,
     

        if newBindings:
            ## if there is only one LHS statement, add RHS as new fact
            if len(rule.lhs) == 1:
                newFact = Fact(instantiate(rule.rhs, newBindings), [[fact, rule]])
                rule.supports_facts.append(newFact)
                fact.supports_facts.append(newFact)
                newFact.asserted = False
                kb.kb_assert(newFact)



            ## if there are multiple statements on LHS, add new rule with bindings and without 1st el
            else:
                onLHS = []
                for curr in rule.lhs[1:]:
                    onLHS.append(instantiate (curr, newBindings))
                    
                newRule = Rule([onLHS, (instantiate(rule.rhs,newBindings))], [[fact, rule]])
                rule.supports_rules.append(newRule)
                fact.supports_rules.append(newRule)
                newRule.asserted = False
                kb.kb_assert(newRule)        


        
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing            
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
