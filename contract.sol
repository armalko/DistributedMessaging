// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title BountyToken by Artem Malko
 * A simple ERC20 Token with bounty registration and redemption functionality.
 */
contract BountyToken {
    // ---------------------
    // ERC20 State Variables
    // ---------------------
    string public name = "BountyToken";
    string public symbol = "BTK";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    // Balances for each account
    mapping (address => uint256) private _balances;
    // Allowances (for typical ERC20 usage, though not strictly needed in this example)
    mapping (address => mapping (address => uint256)) private _allowances;

    // ---------------------
    // Bounty State Variables
    // ---------------------
    bytes32 public currentBountyHash;  // The stored hash for the current bounty
    bool public bountyActive;          // Whether there is an active bounty

    // ---------------------
    // Events
    // ---------------------
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    // Event for debugging or external watchers
    event BountyRegistered(address indexed registrant, bytes32 indexed bountyHash);
    event BountyRedeemed(address indexed redeemer, string solution);

    // ---------------------
    // Constructor
    // ---------------------
    constructor(uint256 initialSupply) {
        // Mint initialSupply tokens to the contract deployer
        // Adjust for decimals if needed
        totalSupply = initialSupply * (10 ** uint256(decimals));
        _balances[msg.sender] = totalSupply;

        emit Transfer(address(0), msg.sender, totalSupply);
    }

    // ---------------------
    // ERC20 Core Functions
    // ---------------------

    /**
     * @dev Returns the balance of a specific address.
     */
    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    /**
     * @dev Transfer tokens to a specified address.
     */
    function transfer(address recipient, uint256 amount) public returns (bool) {
        _transfer(msg.sender, recipient, amount);
        return true;
    }

    /**
     * @dev Returns the remaining number of tokens that `spender` can spend
     * on behalf of `owner` through transferFrom.
     */
    function allowance(address owner, address spender) public view returns (uint256) {
        return _allowances[owner][spender];
    }

    /**
     * @dev Sets `amount` as the allowance of `spender` over the caller’s tokens.
     */
    function approve(address spender, uint256 amount) public returns (bool) {
        _approve(msg.sender, spender, amount);
        return true;
    }

    /**
     * @dev Transfer tokens on behalf of `sender` to `recipient`, given `sender` has granted allowance.
     */
    function transferFrom(address sender, address recipient, uint256 amount) public returns (bool) {
        uint256 currentAllowance = _allowances[sender][msg.sender];
        require(currentAllowance >= amount, "ERC20: transfer amount exceeds allowance");

        _approve(sender, msg.sender, currentAllowance - amount);
        _transfer(sender, recipient, amount);

        return true;
    }

    // ---------------------
    // Internal Helpers
    // ---------------------
    function _transfer(address sender, address recipient, uint256 amount) internal {
        require(sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");
        require(_balances[sender] >= amount, "ERC20: transfer amount exceeds balance");

        _balances[sender] -= amount;
        _balances[recipient] += amount;

        emit Transfer(sender, recipient, amount);
    }

    function _approve(address owner, address spender, uint256 amount) internal {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    // ---------------------
    // Bounty Functions
    // ---------------------

    /**
     * @dev Register a new bounty by providing a hash (e.g. keccak256 of the solution).
     * This function takes exactly 1 token from the caller and activates the bounty.
     * - The caller must have at least 1 token.
     * - The caller must have approved the contract to spend 1 token on their behalf,
     *   OR hold the tokens themselves (if you decide to simply do `transfer`).
     */
    function registerBounty(bytes32 _bountyHash) external {
        // Transfer exactly 1 token from the caller to this contract
        _transfer(msg.sender, address(this), 1);

        // Update the stored bounty hash and activate the bounty
        currentBountyHash = _bountyHash;
        bountyActive = true;

        emit BountyRegistered(msg.sender, _bountyHash);
    }

    /**
     * @dev Redeem the current bounty by providing the correct solution string
     * whose keccak256 hash matches the currentBountyHash. If correct, the contract
     * sends 1 token to the redeemer.
     */
    function redeemBounty(string calldata solution) external {
        require(bountyActive, "No active bounty");

        // Check if the hash of the solution matches the stored hash
        require(
            keccak256(abi.encodePacked(solution)) == currentBountyHash,
            "Incorrect solution"
        );

        // Mark bounty as redeemed
        bountyActive = false;

        // Transfer 1 token from this contract to the redeemer
        _transfer(address(this), msg.sender, 1);

        emit BountyRedeemed(msg.sender, solution);
    }
}
