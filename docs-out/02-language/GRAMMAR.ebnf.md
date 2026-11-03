---
id: LANG-GRAMMAR-001
title: Grammar (EBNF reconstructed from the parser)
kind: catalog
tier: A
status: draft
run_verification: none
scope_class: CORE
version_pin: v7.6.9
pin_method: "last-commit-history + tree metadata: commit d4d786f message "
canonical_facts: [CF-GRM-001]
sources: [src/System.Management.Automation/engine/parser/Parser.cs]
mirror_cards: [src-mirror/src/System.Management.Automation/engine/parser/_folder.md]
generated_from: [data/parser-methods.json]
---

# Grammar (EBNF reconstructed from the parser)

> STATIC-ONLY — behavior not run-verified. Every production below was written from the parser code (`FACT-SRC`); the `// G` grammar comments in the source were used only as hints. Where code and comment disagree the code wins and the production is marked **[≠G]** (recorded as contradiction CON-004). Statement terminators and the newline rules are canonical fact CF-GRM-001, stated in §3a.

## 1. Purpose and scope [SPEC]

An implementer-oriented grammar of the PowerShell language as accepted by `Parser.cs`. It describes **syntax**, not semantics; operator precedence levels are in [02.2-parser.md](02.2-parser.md) §7.2 (generated) and [OPERATOR-TABLE.md](OPERATOR-TABLE.md) (planned T28). Tokenizer-mode dependent lexical rules are in [02.1-tokenizer.md](02.1-tokenizer.md); this grammar uses the token names of [TOKEN-CATALOG.md](TOKEN-CATALOG.md).

Notation: `::=` defines; `|` alternative; `[ x ]` optional; `{ x }` zero or more; `( … )` grouping; `'text'` a token by its text; `Name` a `TokenKind` (e.g. `Variable`, `Generic`); lower-case-hyphen names are non-terminals. `nl` = zero or more `NewLine` tokens (`SkipNewlines`); `nls` = zero or more `NewLine` or `Semi` tokens (`SkipNewlinesAndSemicolons`). "Mode" says which tokenizer mode is active while the production is parsed (C = Command, E = Expression, T = TypeName, S = Signature). Each production names its parser method; all methods are in `src/System.Management.Automation/engine/parser/Parser.cs` (line ranges in [02.2-parser.md](02.2-parser.md) §7.1).

## 2. Source map

| path | type | role |
|---|---|---|
| `src/System.Management.Automation/engine/parser/Parser.cs::Parser@L36-L8191` | class | one `*Rule` method per production below |

## 3. Script structure

```ebnf
script-block        ::= [ using-statements ] [ param-block ] nls [ script-block-body ]        (* ScriptBlockRule; using only at top level *)
using-statements    ::= { using-statement }                                                    (* UsingStatementsRule *)
script-block-body   ::= named-block-list | statement-list-and-closer                          (* ScriptBlockBodyRule *)
named-block-list    ::= { nls block-name statement-block }                                    (* NamedBlockListRule *)
block-name          ::= 'begin' | 'process' | 'end' | 'dynamicparam' | 'clean'
param-block         ::= nl [ attribute-list ] nl 'param' nl '(' [ parameter-list ] nl ')'    (* ParamBlockRule; no '(' => not a param block *)
parameter-list      ::= parameter { nl ',' parameter }                                        (* ParameterListRule *)
parameter           ::= nl [ attribute-list ] nl ( Variable | SplattedVariable ) [ nl '=' nl expression ]   (* ParameterRule, mode E, commas disabled *)
attribute-list      ::= { attribute | type-constraint }                                       (* AttributeListRule *)
attribute           ::= '[' type-spec '(' attribute-arguments ')' ']'                         (* AttributeRule *)
type-constraint     ::= '[' type-spec ']'
attribute-arguments ::= attribute-argument { nl ',' attribute-argument }                      (* AttributeArgumentsRule *)
attribute-argument  ::= nl ( simple-name '=' nl expression | nl expression | simple-name )   (* named, positional, or name only => true *)
statement-block     ::= nl '{' [ statement-list ] nl '}'                                      (* StatementBlockRule *)
statement-list      ::= nls { statement nls }                                                 (* StatementListRule; stops at ')' or '}' *)
```

Notes: a stray token at top level that cannot start a statement is an error and is skipped (`CompleteScriptBlockBody`). `Trap` statements are collected separately from other statements. Duplicate named blocks are an error (`DuplicateScriptCommandClause`) but parsing continues.

## 3a. Statement terminators and newlines (canonical fact)

<!--CF:CF-GRM-001-->**Statement and terminator rule.** A statement list is parsed as: skip any run of newlines and semicolons; parse a statement; skip any run of newlines and semicolons; stop when the next token is `)` or `}` or no statement can be parsed. A terminator is **not** required between statements that end with a closing `}` (e.g. `if`, loops, `try`, `function`), because the list only skips optional terminators; a pipeline (or any statement parsed by `PipelineChainRule`) ends at newline, `;`, `)`, `}`, `&&`/`||` (chain), `&` (background) or end of input, and any other token after a complete pipeline element is `UnexpectedToken`. Newlines continue a construct only in these places: after `|`, before a `|` that starts the next line, after `&&` and `||`, after each binary or unary operator and after `,`, after `=` in an assignment, inside `( )`, after `?`/`:` of a ternary, between `}` and `elseif`/`else`/`catch`/`finally`, and after a backtick line continuation handled by the tokenizer.<!--/CF-->

Evidence: `src/System.Management.Automation/engine/parser/Parser.cs::Parser.StatementListRule@L1897-L1944`, `Parser.PipelineChainRule@L5773-L5988`, `Parser.PipelineRule@L5990-L6160`, `Parser.IfStatementRule@L2400-L2541`, `Parser.CatchBlockRule@L5494-L5591`, `Parser.TryStatementRule@L5593-L5670`.

## 4. Statements

```ebnf
statement           ::= [ attribute-list ] ( keyword-statement | labeled-statement | pipeline-chain )   (* StatementRule *)
keyword-statement   ::= if-statement | function-statement | flow-statement | trap-statement
                      | try-statement | data-statement | class-statement | enum-statement
                      | using-statement | block-statement | configuration-statement | dynamic-keyword-statement
labeled-statement   ::= [ Label ] ( switch-statement | foreach-statement | for-statement | while-statement | do-statement )  (* LabeledStatementRule; label before other => pipeline *)
if-statement        ::= 'if' nl '(' pipeline-chain ')' statement-block
                        { nl 'elseif' nl '(' pipeline-chain ')' statement-block } [ nl 'else' statement-block ]   (* IfStatementRule *)
while-statement     ::= 'while' nl '(' nl pipeline-chain nl ')' statement-block             (* WhileStatementRule *)
do-statement        ::= 'do' statement-block nl ( 'while' | 'until' ) nl '(' pipeline-chain nl ')'   (* DoWhileStatementRule *)
for-statement       ::= 'for' nl '(' nl [ pipeline-chain ] [ ';' nl [ pipeline-chain ] [ ';' nl [ pipeline-chain ] ] ] nl ')' statement-block   (* ForStatementRule; three forms *)
foreach-statement   ::= 'foreach' nl { '-parallel' | '-throttlelimit' nl command-argument } nl
                        '(' nl ( Variable | SplattedVariable ) nl 'in' nl pipeline-chain nl ')' statement-block   (* ForeachStatementRule *)
switch-statement    ::= 'switch' nl { switch-flag } ( '(' nl pipeline-chain nl ')' | '-file' nl command-argument ) nl switch-body   (* SwitchStatementRule *)
switch-flag         ::= '-regex' | '-wildcard' | '-exact' | '-casesensitive' | '-parallel'    (* matched by prefix, case-insensitive *)
switch-body         ::= '{' nls { switch-clause nls } '}'
switch-clause       ::= ( 'default' | command-argument-or-primary ) statement-block
try-statement       ::= 'try' statement-block ( catch-clause { catch-clause } [ finally-clause ] | finally-clause )   (* TryStatementRule *)
catch-clause        ::= nl 'catch' [ type-literal { nl ',' nl type-literal } ] statement-block   (* CatchBlockRule *)
finally-clause      ::= nl 'finally' statement-block
trap-statement      ::= 'trap' nl [ type-literal ] statement-block                            (* TrapStatementRule *)
data-statement      ::= 'data' nl [ simple-name ] [ '-supportedcommand' command-name-list ] statement-block   (* DataStatementRule *)
flow-statement      ::= ( 'break' | 'continue' ) [ label-expression ]                        (* BreakStatementRule ContinueStatementRule *)
                      | ( 'return' | 'exit' | 'throw' ) [ pipeline-chain ]                   (* ReturnStatementRule ExitStatementRule ThrowStatementRule [≠G: throw uses pipeline-chain, comment says pipeline] *)
label-expression    ::= simple-name | unary-expression
block-statement     ::= ( 'parallel' | 'sequence' ) statement-block                          (* BlockStatementRule *)
```

Notes (`FACT-SRC`):
- `else`, `elseif`, `catch`, `until` at statement start with earlier errors are eaten; without errors they are treated as command names (`StatementRule`).
- `from`, `define`, `var` at statement start produce `ReservedKeywordNotAllowed`.
- `using` anywhere but the start of the script parses, then reports `UsingMustBeAtStartOfScript`.
- In `if`, the restore point after the last `}` preserves a following newline so hashtable contexts are not swallowed.
- Break/continue accept an optional label expression; `return`/`exit` use `pipeline-chain`.

## 5. Functions, classes, enums, using

```ebnf
function-statement  ::= ( 'function' | 'filter' | 'workflow' ) nl function-name [ function-params ] statement-block   (* FunctionDeclarationRule *)
function-name       ::= command-argument       (* name token may not be punctuation, string, here-string or variable: MissingNameAfterKeyword *)
function-params     ::= nl '(' parameter-list nl ')'                                          (* FunctionParameterDeclarationRule *)
class-statement     ::= [ attribute-list ] 'class' nl simple-name [ nl ':' nl type-name { nl ',' nl type-name } ] nl '{' { class-member } '}'   (* ClassDefinitionRule; mode S for ':' *)
class-member        ::= { attribute | 'hidden' | 'static' } ( property-member | method-member )   (* ClassMemberRule *)
property-member     ::= [ type-constraint ] Variable [ '=' expression ] ( NewLine | ';' | lookahead '}' )
method-member       ::= [ type-constraint ] method-name '(' [ parameter-list ] ')' [ ':' 'base' '(' arguments ')' ] '{' script-block '}'   (* MethodDeclarationRule; base call only for constructors *)
enum-statement      ::= 'enum' nl simple-name [ ':' underlying-type ] nl '{' { enum-member } '}'   (* EnumDefinitionRule *)
enum-member         ::= simple-name [ '=' expression ] ( NewLine | ';' | lookahead '}' )     (* EnumMemberRule *)
using-statement     ::= 'using' ( 'namespace' name [ '=' name ] | 'module' ( name | hashtable ) [ '=' ( name | hashtable ) ]
                      | 'type' name '=' name | 'assembly' name | 'command' name '=' name ) term   (* UsingStatementRule; item must be a constant string, alias rules per directive *)
```

Notes: valid enum underlying types are Byte, Int16, Int32, Int64, SByte, UInt16, UInt32, UInt64 (`ValidUnderlyingTypeCodes`, `src/System.Management.Automation/engine/parser/Parser.cs::Parser.EnumDefinitionRule@L4701-L4820`). Class members: duplicate `hidden`/`static` is `DuplicateQualifier`; two type constraints is `TooManyTypes`.

## 6. Pipelines, chains, commands

```ebnf
pipeline-chain      ::= assignment | pipeline { chain-op nl pipeline } [ '&' ]               (* PipelineChainRule *)
chain-op            ::= '&&' | '||'                                                          (* left nested PipelineChainAst *)
assignment          ::= expression assignment-op nl statement                                (* RHS is a statement; assignment-op has the AssignmentOperator trait *)
pipeline            ::= ( expression { redirection } | command ) { nl '|' nl command }      (* PipelineRule; later elements must be commands *)
command             ::= [ '&' | '.' ] command-name { command-element }                       (* CommandRule, mode C *)
command-name        ::= Generic | Identifier | primary-expression (when preceded by '&' or '.')
command-element     ::= command-parameter | command-argument | redirection | '--%' raw-text
command-parameter   ::= Parameter [ ':' command-argument ]                                   (* UsedColon => the argument follows *)
command-argument    ::= argument-token { ',' nl argument-token }                             (* comma list => ArrayLiteralAst *)
argument-token      ::= Generic | primary-expression | other-token-as-bareword               (* GetCommandArgument *)
redirection         ::= file-redirection command-argument-or-primary | merging-redirection  (* RedirectionRule; '<' not supported *)
```

Notes: a pipeline continues across a newline only after `|` or when the next line starts with `|`. After the first element an expression is `ExpressionsMustBeFirstInPipeline`. Redirections are limited to `CommandBaseAst.MaxRedirections` slots; a stream may be redirected once (`StreamAlreadyRedirected`).

## 7. Expressions

```ebnf
expression          ::= binary-expression [ '?' nl expression nl ':' nl expression ]        (* ExpressionRule; ternary [≠G: branches are full expressions] *)
binary-expression   ::= array-literal { binary-op nl array-literal }                        (* BinaryExpressionRule: precedence climbing, left assoc, levels in 02.2 §7.2 *)
array-literal       ::= unary-expression { ',' nl unary-expression }                         (* ArrayLiteralRule; skipped when commas disabled *)
unary-expression    ::= unary-op nl unary-expression | ',' nl unary-expression
                      | ( '++' | '--' ) nl unary-expression
                      | attribute-or-type-prefix unary-expression                            (* cast or attributed expression *)
                      | primary-expression [ '++' | '--' ]                                   (* UnaryExpressionRule *)
unary-op            ::= '-not' | '!' | '-bnot' | '+' | '-' | '-split' | '-join'
attribute-or-type-prefix ::= { '[' type-spec ']' | attribute }                                (* type literal; with '::' it is a static member target *)
primary-expression  ::= value { member-access | element-access | invocation }               (* PrimaryExpressionRule + CheckPostPrimaryExpressionOperators *)
value               ::= Variable | SplattedVariable | Number | string-literal | expandable-string
                      | '(' nl pipeline-chain nl ')'                                         (* ParenthesizedExpressionRule *)
                      | '$(' statement-list ')' | '@(' statement-list ')'                    (* SubExpressionRule, mode C *)
                      | '@{' hash-body '}' | '{' script-block '}'                            (* HashExpressionRule, ScriptBlockExpressionRule *)
member-access       ::= ( '.' | '::' | '?.' ) nl member-name                                 (* MemberAccessRule; no whitespace before operator *)
member-name         ::= simple-name | string | unary-expression | primary-expression
invocation          ::= member-access '(' [ expression { ',' expression } ] ')' | member-access script-block   (* MemberInvokeRule, InvokeParamParenListRule; generic: '[' type { ',' type } ']' before '(' *)
element-access      ::= ( '[' | '?[' ) nl expression nl ']'                                   (* ElementAccessRule; commas allowed in index *)
hash-body           ::= nl [ hash-entry { ( NewLine | ';' )+ hash-entry } ] nl
hash-entry          ::= key-expression '=' nl statement                                      (* GetKeyValuePair; key = simple-name | unary-expression *)
type-literal        ::= '[' type-spec ']'
type-spec           ::= type-name [ '[' { ',' } ']' | '[' type-spec { ',' type-spec } ']' ] [ ',' assembly-name ]   (* TypeNameRule, mode T; array rank <= 32 *)
```

Notes (`FACT-SRC`):
- Binary operators are the kinds with the `BinaryOperator` trait except `&&`/`||`; operands are `array-literal`, so `1,2 -eq 3` is `(1,2) -eq 3`.
- A leading `[` in `unary-expression` is parsed as a list of attributes/type constraints; one trailing operand makes a cast (`ConvertExpressionAst`) or an attributed expression; a `::` after the type makes it a static member access target (`TypeExpressionAst`).
- `$using:x` in a variable token yields `UsingExpressionAst`.
- `argument` in an invocation is parsed with the comma operator disabled so commas separate arguments.
- Postfix `++`/`--` apply once.

## 8. Contradictions between the in-source grammar comments and the code

| Place | Comment says | Code does |
|---|---|---|
| `ExpressionRule` | ternary branches are `ternary-expression` | branches are full `ExpressionRule` results (right-nested) |
| `ThrowStatementRule` | `'throw' pipeline:opt` | uses `PipelineChainRule` (like `return`/`exit`) |
| `StatementRule` doc | "never returns null" | returns null at end of input |
| `PipelineChainRule` | text "if this feature is not enabled" | the chain operators are always enabled |
| `StatementRule` `statement-terminator` | each statement ends with a terminator | terminator optional, skipped by `StatementListRule` |

Recorded in `CONTRADICTIONS.md` (CON-004, CON-005).

## 9. Open questions / UNVERIFIED

- Productions for `configuration`, dynamic keywords and DSC-specific parsing are summarized only (`EXTENDED`/DSC is out of scope for MicroteamShell).
- Behavior of `Label` before non-loop statements was read (`LabeledStatementRule`) but not exercised.
- All productions are `FACT-SRC` as syntax; their acceptance behavior on edge input is `UNVERIFIED` until run.

Verification: each production re-derived from the method bodies listed (windows W7-W28 in the parser notes) and compared with the `// G` comments extracted by script from `Parser.cs`; differences are the table in §8; method names in comments exist in `data/parser-methods.json` (checked by `validate-refs` on the cited method ranges).
